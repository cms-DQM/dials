import os
import shutil
import tempfile

import paramiko
from scp import SCPClient

from ..env import lxplus_pwd, lxplus_user


class MinimalLXPlusClient:
    SERVER = "lxplus.cern.ch"
    PORT = 22

    def __init__(self, eos_mounted_at: str | None = None):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.SERVER, username=lxplus_user, password=lxplus_pwd)
        self.eos_mounted_at = eos_mounted_at

    def init_proxy(self) -> None:
        _, stdout, _ = self.client.exec_command("voms-proxy-init -voms cms -rfc")
        stdout = stdout.read().decode("utf-8").strip()
        return True if "Your proxy is valid" in stdout else False

    def xrdcp(self, fpath: str, output_dir: str, redirector: str = "root://cms-xrd-global.cern.ch") -> str:
        fname = fpath.replace("/", "_")[1:]
        out_fpath = f"{output_dir}/{fname}"
        command = f"/usr/bin/xrdcp {redirector}/{fpath} {out_fpath}"
        _, stdout, stderr = self.client.exec_command(command)
        stderr = stderr.read().decode("utf-8").strip()
        stdout = stdout.read().decode("utf-8").strip()

        if stderr != "":
            raise Exception(stderr)

        if stdout == "" and stderr == "":
            return out_fpath
        else:
            raise Exception("Unknown error")

    def scp_to_tmp(self, remote_fpath: str) -> str:
        _tmp_dir = tempfile.mkdtemp()
        _fname = "dqmio_ingestion_copy.root"
        tmp_fpath = os.path.join(_tmp_dir, _fname)

        if isinstance(self.eos_mounted_at, str) and os.path.isdir(self.eos_mounted_at):
            remote_fpath = os.path.join(self.eos_mounted_at, remote_fpath)
            shutil.copy(remote_fpath, tmp_fpath)
        else:
            scp = SCPClient(self.client.get_transport())
            scp.get(remote_fpath, tmp_fpath)

        return tmp_fpath

    def ls(self, remote_path: str) -> list:
        _, stdout, _ = self.client.exec_command(f"ls {remote_path}")
        return stdout.read().decode("utf-8").strip().split("\n")

    def __enter__(self) -> "MinimalLXPlusClient":
        return self

    def __exit__(self, exc_type, exc_val, traceback) -> None:
        self.close()

    def close(self) -> None:
        self.client.close()
