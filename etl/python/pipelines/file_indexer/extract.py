from ...common.dbs_client import MinimalDBSClient
from ...config import dev_env_label, era_cmp_pattern
from ...env import app_env, cert_fpath, key_fpath, mocked_dbs_fpath


def extract(workspace: dict) -> list:
    dbs = (
        MinimalDBSClient(cert_fpath, key_fpath)
        if app_env != dev_env_label
        else MinimalDBSClient(None, None, True, mocked_dbs_fpath)
    )
    files = []
    for pd_name in workspace["primary_datasets"]:
        dt_pattern = f"/{pd_name}/{era_cmp_pattern}/DQMIO"
        response = dbs.get(endpoint="files", params={"dataset": dt_pattern, "detail": 1})
        files.extend(response)
    return files
