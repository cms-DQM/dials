from ...common.dbs_client import MinimalDBSClient
from ...config import era_cmp_pattern
from ...env import cert_fpath, key_fpath


def extract(workspace: dict) -> list:
    dbs = MinimalDBSClient(cert_fpath, key_fpath)
    datasets = []
    for pd_name in workspace["primary_datasets"]:
        dt_pattern = f"/{pd_name}/{era_cmp_pattern}/DQMIO"
        response = dbs.get(endpoint="datasets", params={"dataset": dt_pattern, "detail": 1})
        datasets.extend(response)
    return datasets
