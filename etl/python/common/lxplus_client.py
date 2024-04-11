import paramiko
from scp import SCPClient


class MinimalLXPlusClient:
    SERVER = "lxplus.cern.ch"

    def __init__(self, lxplus_user: str, lxplus_pwd: str):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.SERVER, username=lxplus_user, password=lxplus_pwd)

    def init_proxy(self) -> None:
        _, stdout, _ = self.client.exec_command("voms-proxy-init -voms cms -rfc")
        stdout = stdout.read().decode("utf-8").strip()
        return True if "Your proxy is valid" in stdout else False

    def xrdcp(self, output_dir: str, fpath: str, redirector: str = "root://cms-xrd-global.cern.ch") -> str:
        """
        If multiple processes are trying to download the same file using xrdcp in the same destination,
        we found ourselves in a race condition, because xrdcp will fail with "Run: [ERROR] Local error: file exists:  (destination)"
        for every process that lost the race.
        """
        fname = fpath.replace("/", "_")[1:]
        out_fpath = f"{output_dir}/{fname}"
        grid_fpath = f"{redirector}/{fpath}"
        command = f"/usr/bin/xrdcp {grid_fpath} {out_fpath}"
        _, stdout, stderr = self.client.exec_command(command)
        stderr = stderr.read().decode("utf-8").strip()
        stdout = stdout.read().decode("utf-8").strip()

        # xrdcp succeeded if stdout and stderr are empty
        if stdout == "" and stderr == "":
            return out_fpath

        raise Exception(f"xrdcp failed for {grid_fpath}. stdout: {stdout} stderr: {stderr}")

    def scp(self, remote_fpath: str, local_fpath: str) -> str:
        scp = SCPClient(self.client.get_transport())
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

    def __enter__(self) -> "MinimalLXPlusClient":
        return self

    def __exit__(self, exc_type, exc_val, traceback) -> None:
        self.close()

    def close(self) -> None:
        self.client.close()
