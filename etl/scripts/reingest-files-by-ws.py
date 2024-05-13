#!/usr/bin/env python

import argparse
import os
import sys


sys.path.insert(0, os.getcwd())

from python.config import priority_era, workspaces
from python.env import conn_str
from python.models import FactFileIndex
from python.models.file_index import StatusCollection
from python.pipelines.file_ingesting.tasks import file_ingesting_pipeline_task
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_files(workspace: str) -> dict:
    ws = next(filter(lambda x: x["name"] == workspace, workspaces), None)
    engine = create_engine(f"{conn_str}/{ws['name']}")
    session = sessionmaker(bind=engine)

    with session() as sess:
        query = sess.query(FactFileIndex).filter(
            FactFileIndex.status.in_([StatusCollection.COPY_ERROR, StatusCollection.ROOTFILE_ERROR])
        )
        results = query.all()
        results = [{k: v for k, v in result.__dict__.items() if k != "_sa_instance_state"} for result in results]

    return [
        {
            "queue_name": ws["priority_queue"] if priority_era in res["logical_file_name"] else ws["bulk_queue"],
            "file_id": res["file_id"],
            "dataset_id": res["dataset_id"],
            "workspace_name": ws["name"],
            "workspace_mes": ws["me_startswith"],
        }
        for res in results
    ]


def schedule_ingestion(files: list[dict]):
    for file in files:
        queue_name = file.pop("queue_name")
        file_ingesting_pipeline_task.apply_async(kwargs=file, queue=queue_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Re-download files script.")
    parser.add_argument("--workspace", help="Workspace name.")
    args = parser.parse_args()

    schedule_ingestion(get_files(args.workspace))
