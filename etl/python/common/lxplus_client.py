import logging

import paramiko
from scp import SCPClient

from .lxplus_exceptions import (
    XrdcpBadRootFileError,
    XrdcpNoServersAvailableToReadFileError,
    XrdcpTimeoutError,
    XrdcpUnknownError,
)


logging.getLogger("paramiko").setLevel(logging.WARNING)


class MinimalLXPlusClient:
    SERVER = "lxplus.cern.ch"
    ERROR_MSG_3011 = "[3011] No servers are available to read the file."

    def __init__(self, lxplus_user: str, lxplus_pwd: str, timeout: int = 5 * 60):
        self.timeout = timeout
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.SERVER, username=lxplus_user, password=lxplus_pwd)

    def init_proxy(self) -> None:
        _, stdout, _ = self.client.exec_command(f"/usr/bin/timeout {self.timeout} voms-proxy-init -voms cms -rfc")

        return_code = stdout.channel.recv_exit_status()
        if return_code == 124:
            raise Exception(f"Voms proxy init timed out after {self.timeout} seconds")

        stdout = stdout.read().decode("utf-8").strip()
        return True if "Your proxy is valid" in stdout else False

    def xrdcp(self, output_dir: str, logical_file_name: str, redirector: str = "root://cms-xrd-global.cern.ch") -> str:
        """
        If multiple processes are trying to download the same file using xrdcp in the same destination,
        we found ourselves in a race condition, because xrdcp will fail with "Run: [ERROR] Local error: file exists:  (destination)"
        for every process that lost the race.
        """
        fname = logical_file_name.replace("/", "_")[1:]
        out_fpath = f"{output_dir}/{fname}"
        grid_fpath = f"{redirector}/{logical_file_name}"
        command = f"/usr/bin/timeout {self.timeout} /usr/bin/xrdcp {grid_fpath} {out_fpath}"
        _, stdout, stderr = self.client.exec_command(command)
        return_code = stdout.channel.recv_exit_status()
        stderr = stderr.read().decode("utf-8").strip()
        stdout = stdout.read().decode("utf-8").strip()

        if self.ERROR_MSG_3011 in stderr:
            raise XrdcpNoServersAvailableToReadFileError(
                f"xrdcp (exit = {return_code}) file not found on servers. stderr: {stderr}"
            )

        if return_code == 0:
            return out_fpath
        elif return_code == 124:
            self.rm(out_fpath)
            raise XrdcpTimeoutError(
                f"xrdcp (exit = {return_code}) timed out after {self.timeout} seconds for {grid_fpath}"
            )
        else:
            self.rm(out_fpath)
            raise XrdcpUnknownError(f"xrdcp (exit = {return_code}) failed for {grid_fpath}. stderr: {stderr}")

    def validate_root(self, output_dir: str, logical_file_name: str) -> None:
        fname = logical_file_name.replace("/", "_")[1:]
        fpath = f"{output_dir}/{fname}"
        command = (
            f"python3 -c 'import ROOT; fpath = \"{fpath}\"; f = ROOT.TFile(fpath); f.GetUUID().AsString(); f.Close()'"
        )
        _, stdout, stderr = self.client.exec_command(command)
        return_code = stdout.channel.recv_exit_status()
        stderr = stderr.read().decode("utf-8").strip()
        stdout = stdout.read().decode("utf-8").strip()

        if return_code == 1:
            self.rm(fpath)
            raise XrdcpBadRootFileError

    def validate_adler32(self, output_dir: str, logical_file_name: str, adler32: str) -> None:
        fname = logical_file_name.replace("/", "_")[1:]
        fpath = f"{output_dir}/{fname}"
        command = f'python3 -c \'import sys; import zlib; fpath = "{fpath}"; adler32 = "{adler32}"; sys.exit(0 if format(zlib.adler32(open(fpath, "rb").read()), "08x") == adler32 else 1)\''
        _, stdout, _ = self.client.exec_command(command)
        return_code = stdout.channel.recv_exit_status()

        if return_code == 1:
            self.rm(fpath)
            raise XrdcpBadRootFileError

    def scp(self, remote_fpath: str, local_fpath: str) -> str:
        with SCPClient(self.client.get_transport()) as scp:
            scp.get(remote_fpath, local_fpath)

    def ls(self, remote_path: str) -> list:
        _, stdout, _ = self.client.exec_command(f"ls {remote_path}")
        return stdout.read().decode("utf-8").strip().split("\n")

    def is_file(self, remote_fpath: str) -> list:
        _, stdout, _ = self.client.exec_command(f"test -f {remote_fpath} && echo Success")
        stdout = stdout.read().decode("utf-8").strip()
        return True if stdout == "Success" else False

    def is_dir(self, remote_path: str) -> list:
        _, stdout, _ = self.client.exec_command(f"test -d {remote_path} && echo Success")
        stdout = stdout.read().decode("utf-8").strip()
        return True if stdout == "Success" else False

    def mkdir(self, remote_path: str) -> None:
        self.client.exec_command(f"mkdir -p {remote_path}")

    def rm(self, remote_path: str, recursive: bool = False) -> None:
        rm_base = "rm -rf" if recursive else "rm"
        self.client.exec_command(f"{rm_base} {remote_path}")

    def __enter__(self) -> "MinimalLXPlusClient":
        return self

    def __exit__(self, exc_type, exc_val, traceback) -> None:
        self.close()

    def close(self) -> None:
        self.client.close()
