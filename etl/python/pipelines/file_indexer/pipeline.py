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
    file_index: list = extract(workspace)
    file_index: pd.DataFrame = transform(engine, file_index)
    inserted_ids: list = load(engine, file_index)
    inserted_files: list = file_index[file_index.file_id.isin(inserted_ids)].to_dict(orient="records")
    post_load(workspace, inserted_files)
