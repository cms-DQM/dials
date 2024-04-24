from datetime import datetime

import pandas as pd

from ...models.file_index import StatusCollection


def transform(files: list, datasets_ids: dict) -> pd.DataFrame:
    file_index = [
        {
            "file_id": file["file_id"],
            "dataset_id": datasets_ids[file["dataset"]],
            "file_size": file["file_size"],
            "creation_date": datetime.fromtimestamp(file["creation_date"]),
            "last_modification_date": datetime.fromtimestamp(file["last_modification_date"]),
            "logical_file_name": file["logical_file_name"],
            "status": StatusCollection.PENDING,
            "err_trace": None,
        }
        for file in files
    ]
    return pd.DataFrame(sorted(file_index, key=lambda file: file["file_id"]))
