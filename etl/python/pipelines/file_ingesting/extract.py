import os
import os.path
import shutil
import tempfile

from ...env import RAW_LAYERS
from ..utils import clean_file
from .exceptions import PipelineFileNotAvailableError


def extract(logical_file_name: str) -> str:
    """
    Extracts a DQMIO file from RAW LAYER and return the local path
    to the extracted file.
    """
    file_name = logical_file_name.replace("/", "_")[1:]
    tmp_dir = tempfile.mkdtemp()
    tmp_fpath = os.path.join(tmp_dir, file_name)

    # Try to find the file in multiple raw layers
    src_fpaths = [raw_layer + logical_file_name for raw_layer in RAW_LAYERS]
    for src_fpath in src_fpaths:
        if os.path.isfile(src_fpath) is False:
            continue

        try:
            shutil.copy(src_fpath, tmp_fpath)
            break
        except Exception as e:
            if os.path.isfile(tmp_fpath):
                clean_file(tmp_fpath)
            raise e
    else:
        raise PipelineFileNotAvailableError(src_fpath)

    # Well... if the previous function succeeded we should find the file
    # locally in tmp_fpath.
    if os.path.isfile(tmp_fpath) is False:
        raise Exception(f"File {tmp_fpath} does not exist")

    return tmp_fpath
