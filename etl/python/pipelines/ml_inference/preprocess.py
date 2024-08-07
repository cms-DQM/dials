import numpy as np


def preprocess(data: list[dict]) -> tuple:
    results_ = [{"ls_number": result.ls_number, "data": result.data} for result in data]
    sorted_ = sorted(results_, key=lambda x: x["ls_number"])
    test_array = np.vstack([histogram["data"] for histogram in sorted_])
    test_array = test_array.astype(np.float32)
    lss_ = np.vstack([histogram["ls_number"] for histogram in sorted_])
    return lss_, test_array
