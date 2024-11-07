#!/usr/bin/env python

import argparse

from python.config import common_indexer_queue, primary_datasets, priority_era, workspaces
from python.env import conn_str
from python.models import DimMLModelsIndex, FactFileIndex, FactTH1, FactTH2
from python.models.file_index import StatusCollection
from python.pipelines.dataset_indexer.tasks import dataset_indexer_pipeline_task
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


def ingesting_handler(args):
    if args.all and args.status is None:
        raise ValueError("status argument should be defined when --all is used")
    if StatusCollection.FINISHED in args.status and args.me_startswith is None:
        raise ValueError("me_startswith should be set if status is FINISHED")

    workspace = next(filter(lambda x: x["name"] == args.workspace, workspaces), None)

    if args.all:
        files = get_files_by_status(workspace["name"], status=args.status)
    elif args.files_id:
        files = get_files_by_id(workspace["name"], files_id=args.files_id)

    for file in files:
        queue_name = (
            workspace["priority_ingesting_queue"]
            if priority_era in file["logical_file_name"]
            else workspace["bulk_ingesting_queue"]
        )
        task = {
            "file_id": file["file_id"],
            "dataset_id": file["dataset_id"],
            "workspace_name": workspace["name"],
            "workspace_mes": args.me_startswith if args.me_startswith else workspace["me_startswith"],
        }
        file_ingesting_pipeline_task.apply_async(kwargs=task, queue=queue_name)


def clean_parsing_error_handler(args):
    engine = get_engine(args.workspace)
    Session = sessionmaker(bind=engine)  # noqa: N806
    with Session() as session:
        results = session.query(FactFileIndex).filter(FactFileIndex.status == StatusCollection.PARSING_ERROR).all()
        results = [{k: v for k, v in result.__dict__.items() if k != "_sa_instance_state"} for result in results]
        files_id = [res.get("file_id") for res in results]
        if len(files_id) > 0:
            sql1 = delete(FactTH1).where(FactTH1.file_id.in_(files_id))
            sql2 = delete(FactTH2).where(FactTH2.file_id.in_(files_id))
            session.execute(sql1)
            session.execute(sql2)
            session.commit()
            print(f"Files which histograms were delete: {' '.join(files_id)}")

    engine.dispose()
    return files_id


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


def setup_indexing_subparser(subparsers):
    indexing_parser = subparsers.add_parser("indexing", help="Schedule indexing tasks")
    indexing_parser.add_argument("-s", "--start", action="store_true", help="Schedule a dataset indexing task.")
    indexing_parser.set_defaults(handler=indexing_handler)


def setup_ingesting_subparser(subparsers):
    ingesting_parser = subparsers.add_parser("ingesting", help="Schedule ingesting tasks")
    ingesting_parser.add_argument("-w", "--workspace", help="Workspace name to trigger file ingestion.", required=True)
    ingesting_parser.add_argument(
        "-s",
        "--status",
        nargs="+",
        type=str,
        choices=[
            StatusCollection.FILE_NOT_AVAILABLE,
            StatusCollection.COPY_ERROR,
            StatusCollection.ROOTFILE_ERROR,
            StatusCollection.FINISHED,
        ],
        help="List of status used to search files when --all flag is specified.",
    )
    ingesting_parser.add_argument("-m", "--me-startswith", nargs="+", type=str, help="Custom MEs to ingest.")
    ingesting_paser_arg_group = ingesting_parser.add_mutually_exclusive_group(required=True)
    ingesting_paser_arg_group.add_argument(
        "-a", "--all", action="store_true", help="Select all files marked with specified status."
    )
    ingesting_paser_arg_group.add_argument("-f", "--files-id", nargs="+", type=int, help="List of files id.")
    ingesting_parser.set_defaults(handler=ingesting_handler)


def setup_cleaning_subparser(subparsers):
    clean_table_parser = subparsers.add_parser(
        "clean-parsing-error", help="Clean leftover TH1/TH2 entries in DB for jobs that failed in the parsing step."
    )
    clean_table_parser.add_argument(
        "-w", "--workspace", help="Workspace name to trigger file ingestion.", required=True
    )
    clean_table_parser.set_defaults(handler=clean_parsing_error_handler)


def setup_ml_subparser(subparsers):
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


def main():
    parser = argparse.ArgumentParser(description="DIALS etl command line interface")
    subparsers = parser.add_subparsers(dest="command", title="Commands")
    setup_indexing_subparser(subparsers)
    setup_ingesting_subparser(subparsers)
    setup_cleaning_subparser(subparsers)
    setup_ml_subparser(subparsers)
    args = parser.parse_args()

    if hasattr(args, "handler"):
        args.handler(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
