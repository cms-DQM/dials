import pandas as pd
from sqlalchemy import create_engine

from ...env import conn_str
from .extract import extract
from .load import load
from .post_load import post_load
from .transform import transform


def pipeline(workspaces: list, primary_datasets: list) -> None:
    engines = {ws["name"]: create_engine(f"{conn_str}/{ws['name']}") for ws in workspaces}

    for primary_dataset in primary_datasets:
        ws_names = [ws["name"] for ws in workspaces if primary_dataset in ws["primary_datasets"]]
        dataset_index: list = extract(primary_dataset)
        dataset_index: pd.DataFrame = transform(dataset_index)
        for ws_name in ws_names:
            load(engines[ws_name], dataset_index)

    for engine in engines.values():
        engine.dispose()

    post_load(workspaces, primary_datasets)
