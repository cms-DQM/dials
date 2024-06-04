import pandas as pd
from sqlalchemy import create_engine

from ...common.pgsql import plsql_create_dataset_ids_partitions
from ...env import conn_str
from ...models.file_index import FactFileIndex
from ...models.lumisection import FactLumisection
from ...models.run import FactRun
from ...models.th1 import FactTH1
from ...models.th2 import FactTH2
from .extract import extract
from .load import load
from .post_load import post_load
from .transform import transform


PARTITIONED_TABLES = [
    FactFileIndex.__tablename__,
    FactRun.__tablename__,
    FactLumisection.__tablename__,
    FactTH1.__tablename__,
    FactTH2.__tablename__,
]


def pipeline(workspaces: list, primary_datasets: list) -> None:
    engines = {ws["name"]: create_engine(f"{conn_str}/{ws['name']}") for ws in workspaces}

    for primary_dataset in primary_datasets:
        ws_names = [ws["name"] for ws in workspaces if primary_dataset in ws["primary_datasets"]]
        dataset_index: list = extract(primary_dataset)
        dataset_index: pd.DataFrame = transform(dataset_index)
        for ws_name in ws_names:
            inserted_ids = load(engines[ws_name], dataset_index)
            # For each new dataset id inserted we need to create a new partition
            # You can see that the above function only returns the newly added ids
            if len(inserted_ids) > 0:
                with engines[ws_name].connect() as conn:
                    for tbn in PARTITIONED_TABLES:
                        conn.execute(
                            plsql_create_dataset_ids_partitions(), {"dataset_id_list": inserted_ids, "table_name": tbn}
                        )
                        conn.commit()

    for engine in engines.values():
        engine.dispose()

    post_load(workspaces, primary_datasets)
