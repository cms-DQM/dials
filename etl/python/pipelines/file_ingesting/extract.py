import os
import os.path
import shutil
import tempfile

from ...common.lxplus_client import MinimalLXPlusClient
from ...env import eos_landing_zone, lxplus_pwd, lxplus_user, mounted_eos_path
from .utils import clean_file


def extract_from_eos_mount(workspace_name: str, fname: str, landing_path: str, logical_file_name: str, tmp_fpath: str):
    mounted_path = os.path.join(mounted_eos_path, workspace_name)
    does_dir_exists = os.path.isdir(mounted_path)

    if does_dir_exists is False:
        os.makedirs(mounted_path, exist_ok=True)

    mounted_fpath = os.path.join(mounted_path, fname)
    if not os.path.isfile(mounted_fpath):
        with MinimalLXPlusClient(lxplus_user, lxplus_pwd) as client:
            does_dir_exists = client.is_dir(landing_path)
            if does_dir_exists is False:
                client.mkdir(landing_path)

            client.init_proxy()
            client.xrdcp(landing_path, logical_file_name)

    try:
        shutil.copy(mounted_fpath, tmp_fpath)
    except Exception as e:
        if os.path.isfile(tmp_fpath):
            clean_file(tmp_fpath)
        raise e


def extract_from_eos_ssh(fname: str, landing_path: str, logical_file_name: str, tmp_fpath: str):
    landing_fpath = os.path.join(landing_path, fname)
    with MinimalLXPlusClient(lxplus_user, lxplus_pwd) as client:
        does_dir_exists = client.is_dir(landing_path)
        if does_dir_exists is False:
            client.mkdir(landing_path)

        is_file_available = client.is_file(landing_fpath)
        if is_file_available is False:
            client.init_proxy()
            client.xrdcp(landing_path, logical_file_name)

        try:
            client.scp(landing_fpath, tmp_fpath)
        except Exception as e:
            if os.path.isfile(tmp_fpath):
                clean_file(tmp_fpath)
            raise e


def extract(workspace_name: str, logical_file_name: str) -> str:
    """
    Extracts a DQMIO file from EOS and returns the local path to the extracted file.
    If the file is corrupted (i.e. we cannot open it with ROOT), delete the file and raise the error.

    Logic:
    - If EOS is mounted locally we check if the file exists
        - If the file exists we copy it locally
        - Else we download it using xrdcp trough ssh and then copy it locally
    - Else we check if the file exists via ssh
        - If the file exists we copy it using scp
        - Else we download it using xrdcp and then copy it using scp

    TODO: The current solution download a file N times if it is used by multiple workspaces
          this was the fastest solution to implement to avoid the race condition

    - Solution 1:
    ------------------------------------------------------------------------------------------
    This is tricky to implement because we can't have indexer workers for each workspace
    since after the global indexer schedule the download job we need to know how many
    ingestor jobs the download job will schedule.
    ------------------------------------------------------------------------------------------
    Not download the same file to the same location simultaneously, i.e.
    we should add a new pipeline to out ETL workflow: Indexer -> Downloader -> Ingestor
    That is, after indexing each file we schedule download jobs and after finishing the download
    we schedule ingestion jobs for each workspace that would use that file (we should use one queue for each primary dataset).

    - Solution 2:
    ------------------------------------------------------------------------------------------
    This one was tested and it is not reliable multiple processes hanged
    during xrdcp execution and created the lock file simultaneously
    ------------------------------------------------------------------------------------------
    Another solution (this is faster) is to use a lock to make sure only one process can download
    the same file on the same location at the same time. That is, the process that won the race
    will generate a lock file to inform the other process that the file is being downloaded,
    and the processes that lost the race can ignore the xrdcp error and continuously check if the lock file exists.

    """
    fname = logical_file_name.replace("/", "_")[1:]
    tmp_dir = tempfile.mkdtemp()
    tmp_fpath = os.path.join(tmp_dir, fname)
    landing_path = os.path.join(eos_landing_zone, workspace_name)

    if mounted_eos_path:
        extract_from_eos_mount(workspace_name, fname, landing_path, logical_file_name, tmp_fpath)
    else:
        extract_from_eos_ssh(fname, landing_path, logical_file_name, tmp_fpath)

    # Well... if the previous function succeeded we should find the file locally in tmp_fpath.
    if os.path.isfile(tmp_fpath) is False:
        raise Exception(f"File {tmp_fpath} does not exist")

    return tmp_fpath
