import traceback

from sqlalchemy import create_engine

from ...env import conn_str
from ...models.file_index import StatusCollection
from ..ml_inference.pipeline import pipeline as ml_pipeline
from ..utils import clean_file, error_handler
from .exceptions import PipelineCopyError, PipelineRootfileError
from .extract import extract
from .post_load import post_load
from .pre_extract import pre_extract
from .transform_load import transform_load
from .utils import validate_root_file


WORKSPACES_WITH_ML = {
    "jetmet": [
        {
            "file": "model_CHFrac_highPt_Barrel_checkpoint_20240517.onnx",
            "me": "JetMET/Jet/Cleanedak4PFJetsCHS/CHFrac_highPt_Barrel",
            "thr": 0.05,
        },
        {
            "file": "model_CHFrac_highPt_EndCap_checkpoint_20240517.onnx",
            "me": "JetMET/Jet/Cleanedak4PFJetsCHS/CHFrac_highPt_EndCap",
            "thr": 0.05,
        },
        {
            "file": "model_CHFrac_lowPt_Barrel_checkpoint_20240517.onnx",
            "me": "JetMET/Jet/Cleanedak4PFJetsCHS/CHFrac_lowPt_Barrel",
            "thr": 0.05,
        },
        {
            "file": "model_CHFrac_lowPt_EndCap_checkpoint_20240517.onnx",
            "me": "JetMET/Jet/Cleanedak4PFJetsCHS/CHFrac_lowPt_EndCap",
            "thr": 0.05,
        },
        {
            "file": "model_CHFrac_mediumPt_Barrel_checkpoint_20240517.onnx",
            "me": "JetMET/Jet/Cleanedak4PFJetsCHS/CHFrac_mediumPt_Barrel",
            "thr": 0.05,
        },
        {
            "file": "model_CHFrac_mediumPt_EndCap_checkpoint_20240517.onnx",
            "me": "JetMET/Jet/Cleanedak4PFJetsCHS/CHFrac_mediumPt_EndCap",
            "thr": 0.05,
        },
        {"file": "model_MET_2_checkpoint_20240517.onnx", "me": "JetMET/MET/pfMETT1/Cleaned/MET_2", "thr": 0.05},
        {"file": "model_METPhi_checkpoint_20240517.onnx", "me": "JetMET/MET/pfMETT1/Cleaned/METPhi", "thr": 0.05},
        {"file": "model_METSig_checkpoint_20240517.onnx", "me": "JetMET/MET/pfMETT1/Cleaned/METSig", "thr": 0.05},
        {"file": "model_SumET_checkpoint_20240517.onnx", "me": "JetMET/MET/pfMETT1/Cleaned/SumET", "thr": 0.05},
    ]
}


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
    except Exception as e:  # noqa: BLE001
        err_trace = traceback.format_exc()
        error_handler(engine, file_id, err_trace, StatusCollection.INGESTION_COPY_ERROR)
        raise PipelineCopyError from e

    try:
        validate_root_file(fpath)
    except Exception as e:  # noqa: BLE001
        clean_file(fpath)
        err_trace = traceback.format_exc()
        error_handler(engine, file_id, err_trace, StatusCollection.INGESTION_ROOTFILE_ERROR)
        raise PipelineRootfileError from e

    try:
        transform_load(engine, me_pattern, file_id, dataset_id, fpath, last_status)
    except Exception as e:  # noqa: BLE001
        clean_file(fpath)
        err_trace = traceback.format_exc()
        error_handler(engine, file_id, err_trace, StatusCollection.INGESTION_PARSING_ERROR)
        raise e

    # If everything goes well, we can clean the file
    clean_file(fpath)

    # Run ML pipeline for each model if workspace has any models registered
    if workspace_name in WORKSPACES_WITH_ML:
        for model in WORKSPACES_WITH_ML[workspace_name]:
            ml_pipeline(
                workspace_name=workspace_name,
                model_file=model["file"],
                model_thr=model["thr"],
                model_me=model["me"],
                dataset_id=dataset_id,
                file_id=file_id,
            )

    # Finally finishes
    post_load(engine, file_id)
