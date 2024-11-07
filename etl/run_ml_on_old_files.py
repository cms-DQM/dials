#!/usr/bin/env python

import argparse

from python.config import WORKSPACES
from python.env import DATABASE_RUI
from python.models import FactDatasetIndex, FactFileIndex, FactMLBadLumis
from python.models.file_index import StatusCollection
from python.pipelines.file_ingesting.utils import fetch_active_models
from python.pipelines.ml_inference.pipeline import pipeline as ml_pipeline
from python.pipelines.ml_inference.tasks import ml_inference_pipeline_task
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker


def get_ws_bulk_queue_name():
    ws = next(filter(lambda x: x["name"] == args.workspace_name, WORKSPACES), None)
    return ws["bulk_ingesting_queue"]


def get_dataset(engine: Engine, dataset_name: str):
    sess = sessionmaker(bind=engine)
    with sess() as session:
        return session.query(FactDatasetIndex).filter(FactDatasetIndex.dataset == dataset_name).one()


def get_finished_files(engine: Engine, dataset_id: int):
    sess = sessionmaker(bind=engine)
    with sess() as session:
        query = session.query(FactFileIndex).filter(
            FactFileIndex.dataset_id == dataset_id, FactFileIndex.status == StatusCollection.FINISHED
        )
        return query.all()


def get_existing_preds(engine: Engine, models_ids: list[int], dataset_id: int, files_ids: list[int]):
    sess = sessionmaker(bind=engine)
    with sess() as session:
        query = session.query(FactMLBadLumis).filter(
            FactMLBadLumis.model_id.in_(models_ids),
            FactMLBadLumis.dataset_id == dataset_id,
            FactMLBadLumis.file_id.in_(files_ids),
        )
        return [(res.model_id, res.dataset_id, res.file_id) for res in query.all()]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple script to trigger ML jobs in old files")
    parser.add_argument("-w", "--workspace-name", type=str, required=True)
    parser.add_argument("-d", "--dataset-name", type=str, required=True)
    parser.add_argument("-n", "--no-queue", action="store_true")
    args = parser.parse_args()

    queue = get_ws_bulk_queue_name()
    engine = create_engine(f"{DATABASE_RUI}/{args.workspace_name}")
    dataset = get_dataset(engine, args.dataset_name)
    files = get_finished_files(engine, dataset.dataset_id)
    active_models = fetch_active_models(engine)
    existing_preds = get_existing_preds(
        engine, [model.model_id for model in active_models], dataset.dataset_id, [file.file_id for file in files]
    )
    for file in files:
        for model in active_models:
            pred_tuple = (model.model_id, dataset.dataset_id, file.file_id)
            if pred_tuple in existing_preds:
                print("IGNORING", pred_tuple)
                continue
            kwargs = {
                "workspace_name": args.workspace_name,
                "model_id": model.model_id,
                "model_file": model.filename,
                "target_me": model.target_me,
                "dataset_id": file.dataset_id,
                "file_id": file.file_id,
            }
            if args.no_queue:
                ml_pipeline(**kwargs)
            else:
                ml_inference_pipeline_task.apply_async(kwargs=kwargs, queue=queue)
