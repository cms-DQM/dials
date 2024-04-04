from datetime import datetime
from functools import partial

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import sessionmaker

from ...common.dbs_client import MinimalDBSClient
from ...common.pgsql import copy_expert_onconflict_skip
from ...config import dev_env_label, era_cmp_pattern, priority_era
from ...env import app_env, cert_fpath, conn_str, key_fpath, mocked_dbs_fpath
from ...models import DQMIOIndex
from ...models.dqmio_index import StatusCollection
from ..ingestor.tasks import ingestor_pipeline_task


CHUNK_SIZE = 10000


def extract(workspace: dict) -> list:
    dbs = (
        MinimalDBSClient(cert_fpath, key_fpath)
        if app_env != dev_env_label
        else MinimalDBSClient(None, None, True, mocked_dbs_fpath)
    )
    files = []
    for pd_name in workspace["primary_datasets"]:
        dt_pattern = f"/{pd_name}/{era_cmp_pattern}/DQMIO"
        pd_files = dbs.get(endpoint="files", params={"dataset": dt_pattern, "detail": 1})
        files.extend(pd_files)
    return files


def process_file(file: dict) -> dict:
    return {
        "file_id": file["file_id"],
        "file_size": file["file_size"],
        "era": file["logical_file_name"].split("/")[3].replace("Run", ""),
        "campaign": "-".join(file["dataset"].split("/")[2].split("-")[1:]),
        "dataset": file["dataset"],
        "creation_date": datetime.fromtimestamp(file["creation_date"]),
        "last_modification_date": datetime.fromtimestamp(file["last_modification_date"]),
        "logical_file_name": file["logical_file_name"],
        "status": StatusCollection.INDEXED,
    }


def transform(files: list) -> pd.DataFrame:
    files = [process_file(file) for file in files]
    files = sorted(files, key=lambda file: file["file_id"])
    return pd.DataFrame(files)


def load(engine: Engine, df: pd.DataFrame) -> list:
    pk_name = inspect(DQMIOIndex).primary_key[0].name
    method = partial(copy_expert_onconflict_skip, return_ids=True, pk=pk_name)
    return df.to_sql(
        name=DQMIOIndex.__tablename__, con=engine, if_exists="append", index=False, chunksize=CHUNK_SIZE, method=method
    )


def post_load(engine: Engine, workspace: dict, inserted_files: list) -> None:
    session = sessionmaker(bind=engine)
    sess = session()

    for file in inserted_files:
        sess.query(DQMIOIndex).filter_by(file_id=file["file_id"]).update({"status": StatusCollection.PENDING})
        queue_name = workspace["priority_queue"] if priority_era in file["era"] else workspace["bulk_queue"]
        kwargs = {
            "file_id": file["file_id"],
            "workspace_name": workspace["name"],
            "workspace_mes": workspace["me_startswith"],
        }
        ingestor_pipeline_task.apply_async(kwargs=kwargs, queue=queue_name)

    sess.commit()
    sess.close()


def pipeline(workspace: dict) -> None:
    dm_name = workspace["name"]
    engine = create_engine(f"{conn_str}/{dm_name}")

    files: list = extract(workspace)
    files: pd.DataFrame = transform(files)
    inserted_ids: list = load(engine, files)
    inserted_files: list = files[files.file_id.isin(inserted_ids)].to_dict(orient="records")
    post_load(engine, workspace, inserted_files)
