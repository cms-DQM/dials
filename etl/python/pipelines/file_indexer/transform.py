from datetime import datetime

import pandas as pd
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker

from ...models import FactDatasetIndex
from ...models.file_index import StatusCollection
from ..utils import sqlachemy_asdict


def get_datasets_ids(engine: Engine) -> dict:
    session = sessionmaker(bind=engine)
    with session() as sess:
        datasets = sqlachemy_asdict(sess.query(FactDatasetIndex).all())
        datasets = {dt["dataset"]: dt["dataset_id"] for dt in datasets}
    return datasets


def transform(engine: Engine, files: list) -> pd.DataFrame:
    datasets: dict = get_datasets_ids(engine)
    file_index = [
        {
            "file_id": file["file_id"],
            "dataset_id": datasets[file["dataset"]],
            "file_size": file["file_size"],
            "creation_date": datetime.fromtimestamp(file["creation_date"]),
            "last_modification_date": datetime.fromtimestamp(file["last_modification_date"]),
            "logical_file_name": file["logical_file_name"],
            "status": StatusCollection.PENDING,
            "err_trace": None,
        }
        for file in files
    ]
    file_index = pd.DataFrame(sorted(file_index, key=lambda file: file["file_id"]))

    return file_index
