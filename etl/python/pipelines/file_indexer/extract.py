from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker

from ...common.dbs_client import MinimalDBSClient
from ...config import dev_env_label
from ...env import ENV, GRID_CERT_FPATH, GRID_CERT_KEY_FPATH, MOCKED_DBS_FPATH
from ...models import FactDatasetIndex
from ..utils import sqlachemy_asdict


def extract(primary_dataset: dict) -> list:
    dbs = (
        MinimalDBSClient(primary_dataset["dbs_instance"], GRID_CERT_FPATH, GRID_CERT_KEY_FPATH)
        if ENV != dev_env_label
        else MinimalDBSClient("fake", None, None, True, MOCKED_DBS_FPATH)
    )
    return dbs.get(endpoint="files", params={"dataset": primary_dataset["dbs_pattern"], "detail": 1})


def extract_datasets_ids(engine: Engine) -> dict:
    session = sessionmaker(bind=engine)
    with session() as sess:
        datasets = sqlachemy_asdict(sess.query(FactDatasetIndex).all())
        datasets = {dt["dataset"]: dt["dataset_id"] for dt in datasets}
    return datasets
