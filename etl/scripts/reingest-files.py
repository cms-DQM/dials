#!/usr/bin/env python

import logging
import os
import sys


sys.path.insert(0, os.getcwd())

from python.config import priority_era, workspaces
from python.env import conn_str
from python.models import FactFileIndex, FactTH1, FactTH2
from python.models.file_index import StatusCollection
from python.pipelines.file_ingesting.tasks import file_ingesting_pipeline_task
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker


logging.basicConfig(
    format="[%(asctime)s.%(msecs)03d] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def clean_histograms(workspace: dict) -> list[dict]:
    engine = create_engine(f"{conn_str}/{workspace['name']}")
    session = sessionmaker(bind=engine)

    with session() as sess:
        results = sess.query(FactFileIndex).filter(FactFileIndex.status == StatusCollection.PARSING_ERROR).all()
        index_to_remove = [
            {k: v for k, v in result.__dict__.items() if k != "_sa_instance_state"} for result in results
        ]
        file_ids = [res.get("file_id") for res in index_to_remove]
        if len(file_ids) > 0:
            sql1 = delete(FactTH1).where(FactTH1.file_id.in_(file_ids))
            sql2 = delete(FactTH2).where(FactTH2.file_id.in_(file_ids))
            result1 = sess.execute(sql1)
            sql1_count = result1.rowcount
            result2 = sess.execute(sql2)
            sql2_count = result2.rowcount
            sess.commit()
            msg = f"Deleted {sql1_count+sql2_count} histogram(s) before triggering re-ingestion..."
            logger.info(msg)

    engine.dispose()
    return index_to_remove


def trigger_etl_jobs(files: list[dict]) -> None:
    msg = f"Re-scheduling ETL job(s) of {len(files)} file(s)..."
    logger.info(msg)
    for file in files:
        queue_name = (
            workspace["priority_queue"] if priority_era in file["logical_file_name"] else workspace["bulk_queue"]
        )
        kwargs = {
            "file_id": file["file_id"],
            "dataset_id": file["dataset_id"],
            "workspace_name": workspace["name"],
            "workspace_mes": workspace["me_startswith"],
        }
        file_ingesting_pipeline_task.apply_async(kwargs=kwargs, queue=queue_name)


if __name__ == "__main__":
    for workspace in workspaces:
        files = clean_histograms(workspace)
        if len(files) == 0:
            continue
        trigger_etl_jobs(files)
        logger.info("Done.\n")
