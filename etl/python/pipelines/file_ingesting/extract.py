import os
import os.path
import shutil
import tempfile

from ...common.lxplus_client import MinimalLXPlusClient
from ...env import eos_landing_zone, lxplus_pwd, lxplus_user, mounted_eos_path
from ..utils import clean_file


def extract_locally(primary_dataset: str, file_name: str, target_fpath: str) -> None:
    local_landing_dir = os.path.join(mounted_eos_path, primary_dataset)
    local_file_path = os.path.join(local_landing_dir, file_name)

    try:
        shutil.copy(local_file_path, target_fpath)
    except FileNotFoundError:
        # If your are trying to ingest a file that is not mounted locally
        # or is not in the samples directory, we can copy it from lxplus here
        extract_through_lxplus(primary_dataset, file_name, local_file_path)
        extract_locally(primary_dataset, file_name, target_fpath)
    except Exception as e:
        if os.path.isfile(target_fpath):
            clean_file(target_fpath)
        raise e


def extract_through_lxplus(primary_dataset: str, file_name: str, target_fpath: str) -> None:
    remote_landing_dir = os.path.join(eos_landing_zone, primary_dataset)
    remote_file_path = os.path.join(remote_landing_dir, file_name)

    with MinimalLXPlusClient(lxplus_user, lxplus_pwd) as client:
        try:
            client.scp(remote_file_path, target_fpath)
        except Exception as e:
            if os.path.isfile(target_fpath):
                clean_file(target_fpath)
            raise e


def extract(logical_file_name: str) -> str:
    """
    Extracts a DQMIO file from EOS and returns the local path to the extracted file.
    If the file is corrupted (i.e. we cannot open it with ROOT), delete the file and raise the error.
    """
    file_name = logical_file_name.replace("/", "_")[1:]
    primary_dataset = logical_file_name.split("/")[4]
    tmp_dir = tempfile.mkdtemp()
    tmp_fpath = os.path.join(tmp_dir, file_name)

    # Download the file to tmp_fpath
    if mounted_eos_path and os.path.isdir(mounted_eos_path):
        extract_locally(primary_dataset, file_name, tmp_fpath)
    else:
        extract_through_lxplus(primary_dataset, file_name, tmp_fpath)

    # Well... if the previous function succeeded we should find the file locally in tmp_fpath.
    if os.path.isfile(tmp_fpath) is False:
        raise Exception(f"File {tmp_fpath} does not exist")

    return tmp_fpath
