from ...common.dbs_client import MinimalDBSClient
from ...env import GRID_CERT_FPATH, GRID_CERT_KEY_FPATH


def extract(primary_dataset: dict) -> list:
    dbs = MinimalDBSClient(primary_dataset["dbs_instance"], GRID_CERT_FPATH, GRID_CERT_KEY_FPATH)
    return dbs.get(
        endpoint="datasets", params={"dataset": primary_dataset["dbs_pattern"], "detail": 1, "dataset_access_type": "*"}
    )
