#!/usr/bin/env python

import argparse
import os
import sys


sys.path.insert(0, os.getcwd())

from python.config import pds_queues, priority_era, workspaces
from python.env import conn_str
from python.models import FactFileIndex
from python.models.file_index import StatusCollection
from python.pipelines.file_downloader.tasks import file_downloader_pipeline_task
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_download_error_files() -> dict:
    wss_by_id = {}
    for workspace in workspaces:
        print(f"Checking workspace {workspace['name']}...")
        engine = create_engine(f"{conn_str}/{workspace['name']}")
        session = sessionmaker(bind=engine)
        with session() as sess:
            query = sess.query(FactFileIndex).filter(FactFileIndex.status == StatusCollection.DOWNLOAD_ERROR)
            results = query.all()
            results = [{k: v for k, v in result.__dict__.items() if k != "_sa_instance_state"} for result in results]
            for result in results:
                file_id = result["file_id"]
                if file_id not in wss_by_id:
                    wss_by_id[file_id] = {"dataset_id": None, "logical_file_name": None, "wss": []}
                wss_by_id[file_id]["wss"].append(workspace["name"])
                wss_by_id[file_id]["dataset_id"] = result["dataset_id"]
                wss_by_id[file_id]["logical_file_name"] = result["logical_file_name"]
        engine.dispose()
    return wss_by_id


def get_files_to_requeue(files_ids: list[int]) -> dict:
    wss_by_id = {}
    for workspace in workspaces:
        print(f"Checking workspace {workspace['name']}...")
        engine = create_engine(f"{conn_str}/{workspace['name']}")
        session = sessionmaker(bind=engine)
        with session() as sess:
            query = sess.query(FactFileIndex).filter(FactFileIndex.file_id.in_(files_ids))
            results = query.all()
            results = [{k: v for k, v in result.__dict__.items() if k != "_sa_instance_state"} for result in results]
            for result in results:
                file_id = result["file_id"]
                if file_id not in wss_by_id:
                    wss_by_id[file_id] = {"dataset_id": None, "logical_file_name": None, "wss": []}
                wss_by_id[file_id]["wss"].append(workspace["name"])
                wss_by_id[file_id]["dataset_id"] = result["dataset_id"]
                wss_by_id[file_id]["logical_file_name"] = result["logical_file_name"]
        engine.dispose()
    return wss_by_id


def requeue_download_jobs(wss_by_id: dict) -> None:
    for file_id, item in wss_by_id.items():
        queue_key = "priority_queue" if priority_era in item["logical_file_name"] else "bulk_queue"
        primary_dataset = item["logical_file_name"].split("/")[4]
        queue_name = pds_queues[primary_dataset][queue_key]
        file_downloader_pipeline_task.apply_async(
            kwargs={
                "dataset_id": item["dataset_id"],
                "file_id": file_id,
                "logical_file_name": item["logical_file_name"],
                "wss": [
                    {
                        "name": ws_name,
                        "mes": next(filter(lambda x: x["name"] == ws_name, workspaces), None)["me_startswith"],
                        "p_queue": next(filter(lambda x: x["name"] == ws_name, workspaces), None)["priority_queue"],
                        "b_queue": next(filter(lambda x: x["name"] == ws_name, workspaces), None)["bulk_queue"],
                    }
                    for ws_name in item["wss"]
                ],
            },
            queue=queue_name,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Re-download files script.")
    parser.add_argument(
        "--all", action="store_true", help="A flag to re-download all failed files across all workspaces."
    )
    parser.add_argument("--file-ids", nargs="+", type=int, help="List of file ids to re-download.")
    args = parser.parse_args()

    if args.all:
        wss_by_id: dict = get_download_error_files()
    elif args.file_ids:
        wss_by_id: dict = get_files_to_requeue(args.file_ids)
    else:
        raise Exception("Boolean flag 'all' must be true or 'file-ids' args must be a list of integers.")

    requeue_download_jobs(wss_by_id)
