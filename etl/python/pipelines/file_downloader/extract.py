import os
import os.path

from ...common.lxplus_client import MinimalLXPlusClient
from ...env import eos_landing_zone, lxplus_pwd, lxplus_user, mounted_eos_path


def setup_landing_dir(client: MinimalLXPlusClient, landing_dir: str) -> None:
    does_dir_exists = client.is_dir(landing_dir)
    if does_dir_exists is False:
        client.mkdir(landing_dir)


def extract(logical_file_name: str) -> None:
    file_name = logical_file_name.replace("/", "_")[1:]
    primary_dataset = logical_file_name.split("/")[4]

    # If EOS is mounted locally we can first check if file exists before SSHing
    if mounted_eos_path and os.path.isdir(mounted_eos_path):
        local_landing_dir = os.path.join(mounted_eos_path, primary_dataset)
        local_file_path = os.path.join(local_landing_dir, file_name)
        if os.path.isfile(local_file_path):
            return

    # SSHing if EOS is not mounted locally or file does not exist
    remote_landing_dir = os.path.join(eos_landing_zone, primary_dataset)
    remote_file_path = os.path.join(remote_landing_dir, file_name)
    with MinimalLXPlusClient(lxplus_user, lxplus_pwd) as client:
        setup_landing_dir(client, remote_landing_dir)
        if client.is_file(remote_file_path):
            return
        client.init_proxy()
        client.xrdcp(remote_landing_dir, logical_file_name)
