import traceback

from sqlalchemy import create_engine

from ...common.lxplus_client import XrdcpNoServersAvailableToReadFileError
from ...config import priority_era
from ...env import conn_str
from ...models.file_index import StatusCollection
from ..file_ingesting.tasks import file_ingesting_pipeline_task
from ..utils import error_handler
from .extract import extract
from .post_download import post_download
from .pre_extract import pre_extract


def pipeline(
    dataset_id: int,
    file_id: int,
    logical_file_name: str,
    wss: list[dict],
) -> None:
    engines = {ws["name"]: create_engine(f"{conn_str}/{ws['name']}") for ws in wss}
    for ws in wss:
        pre_extract(engines[ws["name"]], file_id)

    try:
        extract(logical_file_name)
    except Exception as e:
        err_status = (
            StatusCollection.DOWNLOAD_FILE_NOT_AVAILABLE
            if isinstance(e, XrdcpNoServersAvailableToReadFileError)
            else StatusCollection.DOWNLOAD_ERROR
        )
        err_trace = traceback.format_exc()
        for ws in wss:
            error_handler(engines[ws["name"]], file_id, err_trace, err_status)
            engines[ws["name"]].dispose()
        raise e

    for ws in wss:
        post_download(engines[ws["name"]], file_id)
        queue_name = ws["p_queue"] if priority_era in logical_file_name else ws["b_queue"]
        kwargs = {
            "file_id": file_id,
            "dataset_id": dataset_id,
            "workspace_name": ws["name"],
            "workspace_mes": ws["mes"],
        }
        file_ingesting_pipeline_task.apply_async(kwargs=kwargs, queue=queue_name)
