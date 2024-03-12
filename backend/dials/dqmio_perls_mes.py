import re

import requests


URL = "https://github.com/cms-sw/cmssw/raw/master/DQMServices/Core/python/nanoDQMIO_perLSoutput_cff.py"
STARTS_STR = "vstring(*("
ENDS_STR = ")))"


def _get_cmssw_script() -> str:
    req = requests.get(URL, timeout=30)
    req.raise_for_status()
    return req.text


def _std_script_text(text: str) -> str:
    text = text.strip().replace("\n", "")
    return re.sub(r"\s+", "", text)


def _extract_mes(text: str) -> list:
    starts = text.index(STARTS_STR) + len(STARTS_STR)
    ends = text.index(ENDS_STR)
    mes = text[starts:ends].split(",")
    mes = [me.replace('"', "") for me in mes]
    mes = [me for me in mes if me != ""]
    return mes


def get_monitoring_elements_names() -> list:
    text = _get_cmssw_script()
    text = _std_script_text(text)
    return _extract_mes(text)
