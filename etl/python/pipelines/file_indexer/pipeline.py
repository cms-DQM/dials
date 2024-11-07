import pandas as pd
from sqlalchemy import create_engine

from ...config import priority_era
from ...env import DATABASE_RUI
from ..file_ingesting.tasks import file_ingesting_pipeline_task
from .extract import extract, extract_datasets_ids
from .load import load
from .transform import transform


def pipeline(workspaces: list, primary_datasets: list) -> None:
    engines = {ws["name"]: create_engine(f"{DATABASE_RUI}/{ws['name']}") for ws in workspaces}

    for primary_dataset in primary_datasets:
        workspaces_with_pd = [ws for ws in workspaces if primary_dataset in ws["primary_datasets"]]
        file_index: list = extract(primary_dataset)

        # Since all workspaces share the same PD, we can get the datasets_ids from one ws
        ws_sample = workspaces_with_pd[0]["name"]
        datasets_ids: dict = extract_datasets_ids(engines[ws_sample])

        # Transfom
        file_index: pd.DataFrame = transform(file_index, datasets_ids)

        # Insert the file index in each workspace that uses it
        for workspace in workspaces_with_pd:
            ws_name = workspace["name"]
            inserted_ids: list = load(engines[ws_name], file_index)
            inserted_files: list = file_index[file_index.file_id.isin(inserted_ids)].to_dict(orient="records")
            for file in inserted_files:
                dataset_id = file["dataset_id"]
                file_id = file["file_id"]
                logical_file_name = file["logical_file_name"]
                queue_name = (
                    workspace["priority_ingesting_queue"]
                    if priority_era in logical_file_name
                    else workspace["bulk_ingesting_queue"]
                )
                kwargs = {
                    "file_id": file_id,
                    "dataset_id": dataset_id,
                    "workspace_name": ws_name,
                    "workspace_mes": workspace["me_startswith"],
                }
                file_ingesting_pipeline_task.apply_async(kwargs=kwargs, queue=queue_name)

    for engine in engines.values():
        engine.dispose()
