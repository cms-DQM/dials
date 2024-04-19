import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine

from ...env import conn_str
from .extract import extract
from .load import load
from .post_load import post_load
from .transform import transform


def pipeline(workspace: dict) -> None:
    engine: Engine = create_engine(f"{conn_str}/{workspace['name']}")
    dataset_index: list = extract(workspace)
    dataset_index: pd.DataFrame = transform(dataset_index)
    load(engine, dataset_index)
    post_load(workspace)
