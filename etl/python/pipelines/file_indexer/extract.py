from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker

from ...common.dbs_client import MinimalDBSClient
from ...config import dev_env_label, era_cmp_pattern
from ...env import app_env, cert_fpath, key_fpath, mocked_dbs_fpath
from ...models import FactDatasetIndex
from ..utils import sqlachemy_asdict


def extract(primary_dataset: str) -> list:
    dbs = (
        MinimalDBSClient(cert_fpath, key_fpath)
        if app_env != dev_env_label
        else MinimalDBSClient(None, None, True, mocked_dbs_fpath)
    )
    dt_pattern = f"/{primary_dataset}/{era_cmp_pattern}/DQMIO"
    return dbs.get(endpoint="files", params={"dataset": dt_pattern, "detail": 1})


def extract_datasets_ids(engine: Engine) -> dict:
    session = sessionmaker(bind=engine)
    with session() as sess:
        datasets = sqlachemy_asdict(sess.query(FactDatasetIndex).all())
        datasets = {dt["dataset"]: dt["dataset_id"] for dt in datasets}
    return datasets
