import traceback

from sqlalchemy import create_engine

from ...env import conn_str
from ...models.file_index import StatusCollection
from ..ml_inference.pipeline import pipeline as ml_pipeline
from ..utils import clean_file, error_handler
from .exceptions import PipelineCopyError, PipelineFileNotAvailableError, PipelineRootfileError
from .extract import extract
from .post_load import post_load
from .pre_extract import pre_extract
from .transform_load import transform_load
from .utils import fetch_active_models, validate_root_file


def pipeline(workspace_name: str, workspace_mes: str, file_id: int, dataset_id: int):
    """
    Note: always re-raise exceptions to mark the task as failed in celery broker
    """
    me_pattern = f"({'|'.join(workspace_mes)}).*"
    engine = create_engine(f"{conn_str}/{workspace_name}")
    logical_file_name, last_status = pre_extract(engine, file_id)

    # This function already clean the leftover root file if download fails
    try:
        fpath = extract(logical_file_name)
    except PipelineFileNotAvailableError as e:
        err_trace = traceback.format_exc()
        error_handler(engine, file_id, err_trace, StatusCollection.FILE_NOT_AVAILABLE)
        raise e
    except Exception as e:  # noqa: BLE001
        err_trace = traceback.format_exc()
        error_handler(engine, file_id, err_trace, StatusCollection.COPY_ERROR)
        raise PipelineCopyError from e

    try:
        validate_root_file(fpath)
    except Exception as e:  # noqa: BLE001
        clean_file(fpath)
        err_trace = traceback.format_exc()
        error_handler(engine, file_id, err_trace, StatusCollection.ROOTFILE_ERROR)
        raise PipelineRootfileError from e

    try:
        transform_load(engine, me_pattern, file_id, dataset_id, fpath, last_status)
    except Exception as e:  # noqa: BLE001
        clean_file(fpath)
        err_trace = traceback.format_exc()
        error_handler(engine, file_id, err_trace, StatusCollection.PARSING_ERROR)
        raise e

    # If everything goes well, we can clean the file
    clean_file(fpath)

    # Run ML pipeline for each model if workspace has any models registered
    active_models = fetch_active_models(engine)
    for model in active_models:
        ml_pipeline(
            workspace_name=workspace_name,
            model_id=model.model_id,
            model_file=model.filename,
            target_me=model.target_me,
            dataset_id=dataset_id,
            file_id=file_id,
        )

    # Finally finishes
    post_load(engine, file_id)
