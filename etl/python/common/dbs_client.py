import json
import os
import re

import requests
from requests.exceptions import SSLError

from ..env import app_env, mocked_dbs_fpath, sa_globus_path


class MinimalDBSClient:
    API_URL = "https://cmsweb-prod.cern.ch:8443/dbs/prod/global/DBSReader"
    CERT = os.path.join(sa_globus_path, "usercert.pem")
    KEY = os.path.join(sa_globus_path, "userkey.pem")  # This key should be open

    def get(self, **kwargs) -> list:
        if app_env == "test":
            return self.__get_mocked(**kwargs)
        else:
            return self.__get_dbs(**kwargs)

    def __get_dbs(self, endpoint: str, params: dict) -> list:
        url = os.path.join(self.API_URL, endpoint)

        # Running this curl request from LXPlus works without -k flag
        try:
            response = requests.get(url, params=params, cert=(self.CERT, self.KEY), timeout=30)
        except SSLError:
            response = requests.get(url, params=params, cert=(self.CERT, self.KEY), verify=False, timeout=30)  # noqa: S501

        response.raise_for_status()
        return response.json()

    def __get_mocked(self, endpoint: str, params: dict) -> list:
        with open(mocked_dbs_fpath) as fd:
            data = json.load(fd)
        response = [elem for elem in data if re.search(params.get("dataset").replace("*", ".*"), elem.get("dataset"))]
        return response
