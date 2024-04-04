import json
import os
import re

import requests
from requests.exceptions import SSLError


TIMEOUT = 30


class MinimalDBSClient:
    API_URL = "https://cmsweb-prod.cern.ch:8443/dbs/prod/global/DBSReader"

    def __init__(
        self,
        cert_fpath: str | None = None,
        key_fpath: str | None = None,
        use_mock: bool = False,
        mock_fpath: str | None = None,
    ) -> None:
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

        url = os.path.join(self.API_URL, endpoint)
        cert = (self.cert_fpath, self.key_fpath)
        try:
            response = requests.get(url, params=params, cert=cert, timeout=TIMEOUT)
        except SSLError:
            # Running this curl request from LXPlus works without -k flag
            # This is here for local testing
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
