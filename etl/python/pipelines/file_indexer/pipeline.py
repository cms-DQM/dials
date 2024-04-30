import pandas as pd
from sqlalchemy import create_engine

from ...config import pds_queues, priority_era
from ...env import conn_str
from ..file_downloader.tasks import file_downloader_pipeline_task
from .extract import extract, extract_datasets_ids
from .load import load
from .transform import transform


def pipeline(workspaces: list, primary_datasets: list) -> None:
    engines = {ws["name"]: create_engine(f"{conn_str}/{ws['name']}") for ws in workspaces}

    for primary_dataset in primary_datasets:
        ws_names = [ws["name"] for ws in workspaces if primary_dataset in ws["primary_datasets"]]
        ids_by_ws = {ws["name"]: [] for ws in workspaces if primary_dataset in ws["primary_datasets"]}
        file_index: list = extract(primary_dataset)

        # Since all workspaces share the same PD, we can get the datasets_ids from one ws
        datasets_ids: dict = extract_datasets_ids(engines[ws_names[0]])
        file_index: pd.DataFrame = transform(file_index, datasets_ids)

        # Insert the file index in each workspace that uses it
        for ws_name in ws_names:
            inserted_ids: list = load(engines[ws_name], file_index)
            ids_by_ws[ws_name].extend(inserted_ids)

        # Get list of workspaces that an id was inserted
        wss_by_id = {}
        for key, value in ids_by_ws.items():
            for item in value:
                if item not in wss_by_id:
                    wss_by_id[item] = []
                wss_by_id[item].append(key)

        # Schedule download tasks for multiple workspaces that share the same PD
        inserted_files: list = file_index[file_index.file_id.isin(list(wss_by_id.keys()))].to_dict(orient="records")
        for file in inserted_files:
            queue_key = "priority_queue" if priority_era in file["logical_file_name"] else "bulk_queue"
            queue_name = pds_queues[primary_dataset][queue_key]
            file_downloader_pipeline_task.apply_async(
                kwargs={
                    "dataset_id": file["dataset_id"],
                    "file_id": file["file_id"],
                    "logical_file_name": file["logical_file_name"],
                    "wss": [
                        {
                            "name": ws_name,
                            "mes": next(filter(lambda x: x["name"] == ws_name, workspaces), None)["me_startswith"],
                            "p_queue": next(filter(lambda x: x["name"] == ws_name, workspaces), None)["priority_queue"],
                            "b_queue": next(filter(lambda x: x["name"] == ws_name, workspaces), None)["bulk_queue"],
                        }
                        for ws_name in wss_by_id[file["file_id"]]
                    ],
                },
                queue=queue_name,
            )

    for engine in engines.values():
        engine.dispose()
