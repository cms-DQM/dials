import pandas as pd
from sqlalchemy import create_engine

from ...common.pgsql import copy_expert
from ...env import conn_str
from ...models import FactMLBadLumis, FactTH1, FactTH2
from .extract import extract, extract_me
from .predict import predict
from .preprocess import preprocess


def pipeline(
    workspace_name: str,
    model_id: int,
    model_file: str,
    thr: float,
    target_me: str,
    dataset_id: int,
    file_id: int,
):
    engine = create_engine(f"{conn_str}/{workspace_name}")

    # Extrac me_id and TH dimension if me exists in database
    me = extract_me(engine, target_me)
    if me is None:
        return

    # Extract data
    th_class = FactTH1 if me.dim == 1 else FactTH2
    hists = extract(engine, th_class, dataset_id, file_id, me.me_id)
    if len(hists) == 0:
        return

    # Preprocess data
    lss_, input_data = preprocess(hists)

    # Predictions
    preds = predict(workspace_name, model_file, input_data)

    # Select bad lumis
    bad_lumis = []
    for idx, ls_number in enumerate(lss_.flatten()):
        mse = preds[1][idx]
        if mse >= thr:
            bad_lumis.append(
                {
                    "model_id": model_id,
                    "dataset_id": dataset_id,
                    "file_id": file_id,
                    "run_number": hists[idx].run_number,
                    "ls_number": ls_number,
                    "me_id": me.me_id,
                }
            )

    if len(bad_lumis) == 0:
        return

    # Dump bad lumis if there is any
    bad_lumis = pd.DataFrame(bad_lumis)
    bad_lumis.to_sql(name=FactMLBadLumis.__tablename__, con=engine, if_exists="append", index=False, method=copy_expert)
    engine.dispose()
