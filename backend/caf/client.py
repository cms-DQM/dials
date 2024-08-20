import re
from typing import ClassVar

import requests
from bs4 import BeautifulSoup


TIMEOUT = 30


class CAF:
    CAF_URL = "https://cms-service-dqmdc.web.cern.ch/CAF/certification/"
    ENDPOINTS: ClassVar[dict[str, str]] = {
        "muon": {
            "endpoint": "/",
            "lookup_pattern": r"Cert_Collisions(.*)_(\d{6})_(\d{6})_Muon.json",
        },
        "golden": {
            "endpoint": "/",
            "lookup_pattern": r"Cert_Collisions(.*)_(\d{6})_(\d{6})_Golden.json",
        },
        "dcs": {
            "endpoint": "/DCSOnly_JSONS/dailyDCSOnlyJSON/",
            "lookup_pattern": r"Collisions(.*)_(.*)_(\d{6})_(\d{6})_DCSOnly_TkPx\.json",
        },
    }

    def __init__(self, class_name: str, kind: str):
        self.base_url = self.CAF_URL + class_name + self.ENDPOINTS[kind]["endpoint"]
        self.lookup_pattern = self.ENDPOINTS[kind]["lookup_pattern"]
        self.options = self.__get_options()
        self.latest = self.__select_latest()

    def __parse_html(self, text: str):
        soup = BeautifulSoup(text, "html.parser")
        rows = soup.find_all("img", alt="[   ]")
        response = []
        for row in rows:
            link = row.find_next("a")
            name = link.text
            if not re.match(self.lookup_pattern, name):
                continue
            href = link["href"]
            details = link.next_sibling.strip().split()
            date = f"{details[0]} {details[1]}"
            size = details[2]
            response.append({"name": name, "url": self.base_url + href, "last_modified": date, "size": size})
        return response

    def __get_options(self):
        response = requests.get(self.base_url, timeout=TIMEOUT)
        response.raise_for_status()
        return self.__parse_html(response.text)

    def __select_latest(self):
        return sorted(self.options, key=lambda x: x["last_modified"])[-1]

    def download(self, name: str | None = None, latest: bool = False):
        url = next(filter(lambda x: x["name"] == name, self.options))["url"] if name else self.latest["url"]
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
