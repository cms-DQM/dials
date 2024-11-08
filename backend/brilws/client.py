import logging

import paramiko
from bs4 import BeautifulSoup


logging.getLogger("paramiko").setLevel(logging.WARNING)


class BrilcalcError(Exception):
    pass


class Brilcalc:
    SERVER = "lxplus.cern.ch"
    BRILCONDA = "/cvmfs/cms-bril.cern.ch/brilconda/bin"

    def __init__(self, keytab_usr: str, keytab_pwd: str, brilws_version: int | None = None):
        self.brilws_version = brilws_version
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.SERVER, username=keytab_usr, password=keytab_pwd)

    @staticmethod
    def __parse_lumi_html(html, byls: bool = False, unit: str = "/ub"):
        soup = BeautifulSoup(html, "html.parser")
        full_table = soup.find("table")
        summary_table = full_table.find_next("table")

        # Parse full table into a list[dict]
        header, *body = full_table.find_all("tr")
        header = [elem.text for elem in header.find_all("th")]
        body = [[elem.text for elem in body_elem.find_all("td")] for body_elem in body]
        detailed = [dict(zip(header, body_elem, strict=True)) for body_elem in body]
        for elem in detailed:
            run, fill = elem.pop("run:fill").split(":")
            elem["run"] = int(run)
            elem["fill"] = int(fill)
            elem[f"delivered({unit})"] = float(elem[f"delivered({unit})"])
            elem[f"recorded({unit})"] = float(elem[f"recorded({unit})"])

            # columns that only exists if requesting byls output
            if byls:
                elem["E(GeV)"] = int(elem["E(GeV)"])
                elem["avgpu"] = float(elem["avgpu"])

        # Parse the summary table as a dict
        header, body = summary_table.find_all("tr")
        header = [elem.text for elem in header.find_all("th")]
        body = [elem.text for elem in body.find_all("td")]
        summary = dict(zip(header, body, strict=True))
        summary["nfill"] = int(summary["nfill"])
        summary["nrun"] = int(summary["nrun"])
        summary["nls"] = int(summary["nls"])
        summary["ncms"] = int(summary["ncms"])
        summary[f"totdelivered({unit})"] = float(summary[f"totdelivered({unit})"])
        summary[f"totrecorded({unit})"] = float(summary[f"totrecorded({unit})"])

        return {"detailed": detailed, "summary": summary}

    def lumi(
        self,
        connect: str = "offline",
        fillnum: int | None = None,
        runnumber: int | None = None,
        beamstatus: str | None = None,
        unit: str = "/ub",
        amodetag: str | None = None,
        normtag: str | None = None,
        begin: str | int | None = None,
        end: str | int | None = None,
        output_style: str = "tab",
        byls: bool = False,
    ):
        cmd = "brilcalc lumi"
        if connect:
            cmd += f" -c {connect}"
        if fillnum:
            cmd += f" -f {fillnum}"
        if runnumber:
            cmd += f" -r {runnumber}"
        if beamstatus:
            cmd += f" -b {beamstatus}"
        if unit:
            cmd += f" -u {unit}"
        if amodetag:
            cmd += f" --amodetag {amodetag}"
        if normtag:
            cmd += f" --normtag {normtag}"
        if begin:
            cmd += f" --begin {begin}"
        if end:
            cmd += f" --end {end}"
        if output_style:
            cmd += f" --output-style {output_style}"
        if byls is True:
            cmd += " --byls"

        command = f"""
        export PATH=$HOME/.local/bin:{self.BRILCONDA}:$PATH \\
        && pip install --user --upgrade brilws=={self.brilws_version} \\
        && {cmd}
        """
        _, stdout, stderr = self.client.exec_command(command)
        stdout_text = stdout.read().decode("utf-8")
        stderr_text = stderr.read().decode("utf-8")
        return_code = stdout.channel.recv_exit_status()
        del stdout, stderr

        if return_code != 0:
            raise BrilcalcError(stderr_text)

        return self.__parse_lumi_html(stdout_text, byls, unit)
