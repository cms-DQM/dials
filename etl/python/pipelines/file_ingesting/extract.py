import os
import os.path
import shutil
import tempfile

from ...env import mounted_eos_path
from ..utils import clean_file
from .exceptions import PipelineFileNotAvailableError


def extract(logical_file_name: str) -> str:
    """
    Extracts a DQMIO file from EOS and returns the local path to the extracted file.
    If the file is corrupted (i.e. we cannot open it with ROOT), delete the file and raise the error.
    """
    file_name = logical_file_name.replace("/", "_")[1:]
    tmp_dir = tempfile.mkdtemp()
    tmp_fpath = os.path.join(tmp_dir, file_name)

    # The base path where files are expected to be is `mounted_eos_path`
    # This path is configurable in the environment, you can copy files locally
    # using `scp` and replicated the `logical_file_name` inside your base path
    eos_file_path = mounted_eos_path + logical_file_name
    if os.path.isfile(eos_file_path) is False:
        raise PipelineFileNotAvailableError(eos_file_path)

    try:
        shutil.copy(eos_file_path, tmp_fpath)
    except Exception as e:
        if os.path.isfile(tmp_fpath):
            clean_file(tmp_fpath)
        raise e

    # Well... if the previous function succeeded we should find the file locally in tmp_fpath.
    if os.path.isfile(tmp_fpath) is False:
        raise Exception(f"File {tmp_fpath} does not exist")

    return tmp_fpath
