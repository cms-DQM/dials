from ...common.dbs_client import MinimalDBSClient
from ...env import cert_fpath, key_fpath


def extract(primary_dataset: dict) -> list:
    dbs = MinimalDBSClient(primary_dataset["dbs_instance"], cert_fpath, key_fpath)
    return dbs.get(
        endpoint="datasets", params={"dataset": primary_dataset["dbs_pattern"], "detail": 1, "dataset_access_type": "*"}
    )
