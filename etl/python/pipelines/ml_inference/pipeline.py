import numpy as np
import pandas as pd
from sqlalchemy import create_engine

from ...common.pgsql import copy_expert
from ...env import DATABASE_RUI
from ...models import FactMLBadLumis, FactTH1, FactTH2
from .extract import extract, extract_me
from .predict import predict


def pipeline(
    workspace_name: str,
    model_id: int,
    model_file: str,
    target_me: str,
    dataset_id: int,
    file_id: int,
):
    engine = create_engine(f"{DATABASE_RUI}/{workspace_name}")

    # Extrac me_id and TH dimension if me exists in database
    me = extract_me(engine, target_me)
    if me is None:
        return

    # Extract data
    th_class = FactTH1 if me.dim == 1 else FactTH2
    hists = extract(engine, th_class, dataset_id, file_id, me.me_id)
    if len(hists) == 0:
        return

    # Sort by run_number and ls_number only
    # since dataset_id, file_id and me_id are fixed.
    hists = [{"run_number": hist.run_number, "ls_number": hist.ls_number, "data": hist.data} for hist in hists]
    hists = sorted(hists, key=lambda x: (x["run_number"], x["ls_number"]))
    data = np.vstack([hist.pop("data") for hist in hists]).astype(np.float32)

    # Predictions
    preds = predict(workspace_name, model_file, data)

    # Select bad lumis
    bad_lumis = []
    for idx, hist in enumerate(hists):
        mse = preds[1][idx]
        is_anomaly = bool(preds[2][idx])
        if is_anomaly:
            bad_lumis.append(
                {
                    "model_id": model_id,
                    "dataset_id": dataset_id,
                    "file_id": file_id,
                    "run_number": hist["run_number"],
                    "ls_number": hist["ls_number"],
                    "me_id": me.me_id,
                    "mse": mse,
                }
            )

    if len(bad_lumis) == 0:
        return

    # Dump bad lumis if there is any
    bad_lumis = pd.DataFrame(bad_lumis)
    bad_lumis.to_sql(name=FactMLBadLumis.__tablename__, con=engine, if_exists="append", index=False, method=copy_expert)
    engine.dispose()
