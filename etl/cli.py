#!/usr/bin/env python

import argparse

from python.config import common_indexer_queue, primary_datasets, priority_era, workspaces
from python.env import conn_str
from python.models import DimMLModelsIndex, FactFileIndex, FactTH1, FactTH2
from python.models.file_index import StatusCollection
from python.pipelines.dataset_indexer.tasks import dataset_indexer_pipeline_task
from python.pipelines.file_downloader.tasks import file_downloader_pipeline_task
from python.pipelines.file_ingesting.tasks import file_ingesting_pipeline_task
from sqlalchemy import create_engine, delete
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker


def get_engine(workspace: str) -> Engine:
    return create_engine(f"{conn_str}/{workspace}")


def get_files_by_id(workspace: str, files_id: list[int]) -> None:
    engine = get_engine(workspace)
    Session = sessionmaker(bind=engine)  # noqa: N806
    with Session() as session:
        results = session.query(FactFileIndex).filter(FactFileIndex.file_id.in_(files_id)).all()
        results = [{k: v for k, v in result.__dict__.items() if k != "_sa_instance_state"} for result in results]
    engine.dispose()
    return results


def get_files_by_status(workspace: str, status: str | list[str]) -> None:
    engine = create_engine(f"{conn_str}/{workspace}")
    Session = sessionmaker(bind=engine)  # noqa: N806
    with Session() as session:
        query = session.query(FactFileIndex)
        if isinstance(status, str):
            query = query.filter(FactFileIndex.status == status)
        elif isinstance(status, list):
            query = query.filter(FactFileIndex.status.in_(status))
        results = query.all()
        results = [{k: v for k, v in result.__dict__.items() if k != "_sa_instance_state"} for result in results]
    engine.dispose()
    return results


def downloader_handler(args):
    wss_by_id = {}
    for workspace in workspaces:
        ws_name = workspace["name"]
        if args.all:
            files = get_files_by_status(ws_name, status=StatusCollection.DOWNLOAD_ERROR)
        elif args.file_ids:
            files = get_files_by_id(ws_name, files_id=args.file_ids)
        for result in files:
            file_id = result["file_id"]
            if file_id not in wss_by_id:
                wss_by_id[file_id] = {"dataset_id": None, "logical_file_name": None, "wss": []}
            wss_by_id[file_id]["wss"].append(ws_name)
            wss_by_id[file_id]["dataset_id"] = result["dataset_id"]
            wss_by_id[file_id]["logical_file_name"] = result["logical_file_name"]

    for file_id, item in wss_by_id.items():
        first_ws = next(filter(lambda x: x["name"] == item["wss"][0], workspaces), None)
        queue_key = (
            "priority_downloader_queue" if priority_era in item["logical_file_name"] else "bulk_downloader_queue"
        )
        primary_dataset = item["logical_file_name"].split("/")[4]
        queue_name = next(filter(lambda x: primary_dataset in x["dbs_pattern"], first_ws["primary_datasets"]), None)[
            queue_key
        ]
        file_downloader_pipeline_task.apply_async(
            kwargs={
                "dataset_id": item["dataset_id"],
                "file_id": file_id,
                "logical_file_name": item["logical_file_name"],
                "wss": [
                    {
                        "name": ws_name,
                        "me_startswith": next(filter(lambda x: x["name"] == ws_name, workspaces), None)[
                            "me_startswith"
                        ],
                        "priority_ingesting_queue": next(filter(lambda x: x["name"] == ws_name, workspaces), None)[
                            "priority_ingesting_queue"
                        ],
                        "bulk_ingesting_queue": next(filter(lambda x: x["name"] == ws_name, workspaces), None)[
                            "bulk_ingesting_queue"
                        ],
                    }
                    for ws_name in item["wss"]
                ],
            },
            queue=queue_name,
        )


def ingesting_handler(args):
    if args.all and args.status is None:
        raise ValueError("status argument should be defined when --all is used")
    if StatusCollection.FINISHED in args.status and args.me_startswith is None:
        raise ValueError("me_startswith should be set if status is FINISHED")

    workspace = next(filter(lambda x: x["name"] == args.workspace, workspaces), None)

    if args.all:
        files = get_files_by_status(workspace["name"], status=args.status)
    elif args.file_ids:
        files = get_files_by_status(workspace["name"], files_id=args.files_id)

    tasks = [
        {
            "queue_name": workspace["priority_ingesting_queue"]
            if priority_era in file["logical_file_name"]
            else workspace["bulk_ingesting_queue"],
            "file_id": file["file_id"],
            "dataset_id": file["dataset_id"],
            "workspace_name": workspace["name"],
            "workspace_mes": workspace["me_startswith"],
        }
        for file in files
    ]

    if args.me_startswith:
        tasks = [{**task, "workspace_mes": args.me_startswith} for task in tasks]

    for task in tasks:
        queue_name = task.pop("queue_name")
        file_ingesting_pipeline_task.apply_async(kwargs=task, queue=queue_name)


def clean_parsing_error_handler(args):
    engine = get_engine(args.workspace)
    Session = sessionmaker(bind=engine)  # noqa: N806
    with Session() as session:
        results = (
            session.query(FactFileIndex).filter(FactFileIndex.status == StatusCollection.INGESTION_PARSING_ERROR).all()
        )
        results = [{k: v for k, v in result.__dict__.items() if k != "_sa_instance_state"} for result in results]
        file_ids = [res.get("file_id") for res in results]
        if len(file_ids) > 0:
            sql1 = delete(FactTH1).where(FactTH1.file_id.in_(file_ids))
            sql2 = delete(FactTH2).where(FactTH2.file_id.in_(file_ids))
            session.execute(sql1)
            session.execute(sql2)
            session.commit()
            print(f"Files which histograms were delete: {' '.join(file_ids)}")
    engine.dispose()
    return file_ids


def indexing_handler(args):
    if args.start is True:
        dataset_indexer_pipeline_task.apply_async(
            kwargs={"workspaces": workspaces, "primary_datasets": primary_datasets}, queue=common_indexer_queue
        )


def add_ml_model_to_index_hanlder(args):
    engine = get_engine(args.workspace)
    Session = sessionmaker(bind=engine)  # noqa: N806
    with Session() as session:
        model = DimMLModelsIndex(filename=args.filename, target_me=args.target_me, thr=args.thr, active=args.active)
        session.add(model)
        session.commit()


def main():
    parser = argparse.ArgumentParser(description="DIALS etl command line interface")
    subparsers = parser.add_subparsers(dest="command", title="Commands")

    # Indexing command
    indexing_parser = subparsers.add_parser("indexing", help="Schedule indexing tasks")
    indexing_parser.add_argument("-s", "--start", action="store_true", help="Schedule a dataset indexing task.")
    indexing_parser.set_defaults(handler=indexing_handler)

    # Downloader command
    downloader_parser = subparsers.add_parser("downloader", help="Schedule downloading tasks")
    downloader_paser_arg_group = downloader_parser.add_mutually_exclusive_group(required=True)
    downloader_paser_arg_group.add_argument(
        "-a", "--all", action="store_true", help="Select all files marked with DOWNLOAD_ERROR."
    )
    downloader_paser_arg_group.add_argument("-f", "--file-ids", nargs="+", type=int, help="List of files id")
    downloader_parser.set_defaults(handler=downloader_handler)

    # Ingesting command
    ingesting_parser = subparsers.add_parser("ingesting", help="Schedule ingesting tasks")
    ingesting_parser.add_argument("-w", "--workspace", help="Workspace name to trigger file ingestion.", required=True)
    ingesting_parser.add_argument(
        "-s",
        "--status",
        nargs="+",
        type=str,
        choices=[
            StatusCollection.INGESTION_COPY_ERROR,
            StatusCollection.INGESTION_ROOTFILE_ERROR,
            StatusCollection.FINISHED,
        ],
        help="List of status used to search files when --all flag is specified.",
    )
    ingesting_parser.add_argument("-m", "--me-startswith", nargs="+", type=str, help="Custom MEs to ingest.")
    ingesting_paser_arg_group = ingesting_parser.add_mutually_exclusive_group(required=True)
    ingesting_paser_arg_group.add_argument(
        "-a", "--all", action="store_true", help="Select all files marked with specified status."
    )
    ingesting_paser_arg_group.add_argument("-f", "--file-ids", nargs="+", type=int, help="List of files id.")
    ingesting_parser.set_defaults(handler=ingesting_handler)

    # Clean command
    clean_table_parser = subparsers.add_parser("clean-parsing-error", help="Schedule downloading tasks")
    clean_table_parser.add_argument(
        "-w", "--workspace", help="Workspace name to trigger file ingestion.", required=True
    )
    clean_table_parser.set_defaults(handler=clean_parsing_error_handler)

    # Register ml model command
    add_ml_model_parser = subparsers.add_parser("add-ml-model-to-index", help="Register ML molde into DB")
    add_ml_model_parser.add_argument("-w", "--workspace", help="Workspace name.", required=True)
    add_ml_model_parser.add_argument("-f", "--filename", help="Model binary filename", required=True)
    add_ml_model_parser.add_argument(
        "-m", "--target-me", help="Monitoring element predicted by the model", required=True
    )
    add_ml_model_parser.add_argument(
        "-t", "--thr", help="Model threshold for anomaly detection", required=True, type=float
    )
    add_ml_model_parser.add_argument("-a", "--active", help="Is the model active?", required=True, type=bool)
    add_ml_model_parser.set_defaults(handler=add_ml_model_to_index_hanlder)

    args = parser.parse_args()

    if hasattr(args, "handler"):
        args.handler(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
