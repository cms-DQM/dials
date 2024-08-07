import json
import os
import re

import requests
import urllib3
from requests.exceptions import SSLError


TIMEOUT = 30


class MinimalDBSClient:
    BASE_URL = "https://cmsweb-prod.cern.ch:8443/dbs/prod"

    def __init__(
        self,
        dbs_instance: str | None = "global",
        cert_fpath: str | None = None,
        key_fpath: str | None = None,
        use_mock: bool = False,
        mock_fpath: str | None = None,
    ) -> None:
        self.reader_url = os.path.join(self.BASE_URL, dbs_instance, "DBSReader")
        self.cert_fpath = cert_fpath
        self.key_fpath = key_fpath  # This key should be open
        self.use_mock = use_mock
        self.mock_fpath = mock_fpath

    def get(self, **kwargs) -> list:
        if self.use_mock:
            return self.__get_mocked(**kwargs)
        else:
            return self.__get_dbs(**kwargs)

    def __get_dbs(self, endpoint: str, params: dict) -> list:
        if self.cert_fpath is None or self.key_fpath is None:
            raise ValueError("Cert or key file path not set")

        url = os.path.join(self.reader_url, endpoint)
        cert = (self.cert_fpath, self.key_fpath)
        try:
            response = requests.get(url, params=params, cert=cert, timeout=TIMEOUT)
        except SSLError:
            # Running this curl request from LXPlus works without -k flag
            # This is here for local testing and for Openshift deployment
            with urllib3.warnings.catch_warnings():
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                response = requests.get(url, params=params, cert=cert, timeout=TIMEOUT, verify=False)  # noqa: S501

        response.raise_for_status()
        return response.json()

    def __get_mocked(self, endpoint: str, params: dict) -> list:
        if self.mock_fpath is None:
            raise ValueError("Mock file path not set")
        with open(self.mock_fpath) as fd:
            response = json.load(fd)
        if params.get("dataset"):
            filter_ptrn = params.get("dataset").replace("*", ".*")
            response = [elem for elem in response if re.search(filter_ptrn, elem.get("dataset"))]
        return response
