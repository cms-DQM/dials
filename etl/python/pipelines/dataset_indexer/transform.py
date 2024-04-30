from datetime import datetime

import pandas as pd


def transform(datasets: list) -> pd.DataFrame:
    datasets = [
        {
            "dataset_id": dataset["dataset_id"],
            "dataset": dataset["dataset"],
            "era": dataset["acquisition_era_name"],
            "data_tier": dataset["data_tier_name"],
            "primary_ds_name": dataset["primary_ds_name"],
            "processed_ds_name": dataset["processed_ds_name"],
            "processing_version": dataset["processing_version"],
            "last_modification_date": datetime.fromtimestamp(dataset["last_modification_date"]),
        }
        for dataset in datasets
    ]
    datasets = sorted(datasets, key=lambda file: file["dataset_id"])

    return pd.DataFrame(datasets)
