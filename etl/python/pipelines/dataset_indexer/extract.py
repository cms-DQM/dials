from ...common.dbs_client import MinimalDBSClient
from ...config import era_cmp_pattern
from ...env import cert_fpath, key_fpath


def extract(primary_dataset: str) -> list:
    dbs = MinimalDBSClient(cert_fpath, key_fpath)
    dt_pattern = f"/{primary_dataset}/{era_cmp_pattern}/DQMIO"
    return dbs.get(endpoint="datasets", params={"dataset": dt_pattern, "detail": 1, "dataset_access_type": "*"})
