from functools import partial, reduce

import pandas as pd
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker

from ...common.dqmio_reader import DQMIOReader
from ...common.pgsql import copy_expert, copy_expert_onconflict_update, insert_onconflict_update
from ...config import COMMON_CHUK_SIZE, TH1_TYPES, TH2_CHUNK_SIZE, TH2_TYPES
from ...models import DimMonitoringElements, FactLumisection, FactRun, FactTH1, FactTH2
from ...models.file_index import StatusCollection
from ..utils import list_to_sql_array, sqlachemy_asdict


def transform_load_run(engine: Engine, reader: DQMIOReader, dataset_id: int) -> None:
    run_lumi = reader.index_keys
    runs = reduce(lambda acc, cur: {cur[0]: acc.get(cur[0], 0) + 1}, run_lumi, {})
    runs = [{"run_number": run, "dataset_id": dataset_id, "ls_count": ls_count} for run, ls_count in runs.items()]
    expr = f"ls_count = {FactRun.__tablename__}.ls_count + EXCLUDED.ls_count"
    method = partial(copy_expert_onconflict_update, conflict_key="run_number, dataset_id", expr=expr)
    runs = pd.DataFrame(runs)
    runs.to_sql(
        name=FactRun.__tablename__,
        con=engine,
        if_exists="append",
        index=False,
        chunksize=COMMON_CHUK_SIZE,
        method=method,
    )


def transform_load_lumis(
    engine: Engine, reader: DQMIOReader, me_pattern: str, dataset_id: int, update_on_conflict: bool = False
) -> None:
    run_lumi = reader.index_keys
    lumis = []
    for run, lumi in run_lumi:
        th1_me = reader.get_mes_for_lumi(run, lumi, types=TH1_TYPES, re_pattern=me_pattern)
        th2_me = reader.get_mes_for_lumi(run, lumi, types=TH2_TYPES, re_pattern=me_pattern)
        lumis.append(
            {
                "dataset_id": dataset_id,
                "run_number": run,
                "ls_number": lumi,
                "th1_count": len(th1_me),
                "th2_count": len(th2_me),
            }
        )
    lumis = pd.DataFrame(lumis)

    if update_on_conflict:
        expr = f"th1_count = {FactLumisection.__tablename__}.th1_count + EXCLUDED.th1_count, th2_count = {FactLumisection.__tablename__}.th2_count + EXCLUDED.th2_count"
        method = partial(copy_expert_onconflict_update, conflict_key="dataset_id, run_number, ls_number", expr=expr)
    else:
        method = copy_expert

    lumis.to_sql(
        name=FactLumisection.__tablename__,
        con=engine,
        if_exists="append",
        index=False,
        chunksize=COMMON_CHUK_SIZE,
        method=method,
    )


def transform_mes(reader: DQMIOReader, me_pattern: str) -> list[dict]:
    run_lumi = reader.index_keys
    mes_list = {}
    for run, lumi in run_lumi:
        mes = reader.get_mes_for_lumi(
            run,
            lumi,
            types=(
                *TH1_TYPES,
                *TH2_TYPES,
            ),
            re_pattern=me_pattern,
        )
        for me in mes:
            if me.name not in mes_list.keys():
                dim = 1 if me.type in TH1_TYPES else 2
                mes_list[me.name] = {"count": 0, "dim": dim}
            mes_list[me.name]["count"] += 1

    return [{"me": me_name, **count_dim} for me_name, count_dim in mes_list.items()]


def load_mes(engine: Engine, mes_list: list[dict], set_zero_count: bool = False) -> None:
    expr = f"count = {DimMonitoringElements.__tablename__}.count + EXCLUDED.count"
    method = partial(insert_onconflict_update, conflict_key="me", expr=expr)
    if set_zero_count:
        mes_list = [{**me, "count": 0} for me in mes_list]

    mes_list = pd.DataFrame(mes_list)
    mes_list.to_sql(
        name=DimMonitoringElements.__tablename__,
        con=engine,
        if_exists="append",
        index=False,
        chunksize=COMMON_CHUK_SIZE,
        method=method,
    )


def transform_load_th(
    th_table: str, engine: Engine, reader: DQMIOReader, me_pattern: str, file_id: int, dataset_id: int
) -> None:
    th_chunk_size = COMMON_CHUK_SIZE if th_table == FactTH1.__tablename__ else TH2_CHUNK_SIZE
    types = TH1_TYPES if th_table == FactTH1.__tablename__ else TH2_TYPES
    reader_func = reader.th1_from_cppyy if th_table == FactTH1.__tablename__ else reader.th2_from_cppyy
    run_lumi = reader.index_keys

    # Get dimensions table to transform fact
    session = sessionmaker(bind=engine)
    with session() as sess:
        mes = sqlachemy_asdict(sess.query(DimMonitoringElements).all())
        mes = {me["me"]: me["me_id"] for me in mes}

    th_list = []
    chunk_count = 0
    for run, lumi in run_lumi:
        me_list = reader.get_mes_for_lumi(run, lumi, types=types, re_pattern=me_pattern)
        for me in me_list:
            th_entry = reader_func(me)
            th_entry["me_id"] = mes[th_entry.pop("me")]
            th_entry = {
                "file_id": file_id,
                "dataset_id": dataset_id,
                "run_number": run,
                "ls_number": lumi,
                **th_entry,
            }
            th_list.append(th_entry)

            chunk_count += 1
            if chunk_count == th_chunk_size:
                th_list = pd.DataFrame(th_list)
                th_list["data"] = th_list.data.apply(list_to_sql_array)
                th_list.to_sql(name=th_table, con=engine, if_exists="append", index=False, method=copy_expert)
                th_list = []
                chunk_count = 0

            del th_entry

    del chunk_count, me_list

    if len(th_list) > 0:
        th_list = pd.DataFrame(th_list)
        th_list["data"] = th_list.data.apply(list_to_sql_array)
        th_list.to_sql(name=th_table, con=engine, if_exists="append", index=False, method=copy_expert)
        del th_list


def transform_load(
    engine: Engine, me_pattern: str, file_id: int, dataset_id: int, fpath: str, last_status: str
) -> pd.DataFrame:
    reader = DQMIOReader(fpath)

    # - First extract all MEs from the DQMIO file and insert into the database with their count equal to 0
    # We need to insert at least their names because the `transform_load_th` expects to retrieve their respective
    # me_id autogenerated when we insert the ME into the database
    # - But why inserting with count field equals to 0?
    # If the pipeline fails during any `transform_load_th`, before ingesting again we need to clean the database
    # if the MEs were inserted with their correct count we would need to "guess" or re-read the root file
    # to correctly subtract the amount MEs from the count field.
    # This way, we know for sure we only need to delete leftover TH1 and TH2 histograms before re-ingesting.
    mes_list: list[dict] = transform_mes(reader, me_pattern)
    load_mes(engine, mes_list, set_zero_count=True)

    # Ingest TH1 and TH2 sequentially
    transform_load_th(FactTH1.__tablename__, engine, reader, me_pattern, file_id, dataset_id)
    transform_load_th(FactTH2.__tablename__, engine, reader, me_pattern, file_id, dataset_id)

    # Now we can update the count field safely, if the pipeline fails in the next steps it is easy to
    # subtract the count field by counting how many histograms were inserted before for this specific file_id
    load_mes(engine, mes_list)

    # This step can fail if we have conflicting data for (dataset_id, run_number, ls_number)
    # Essentially we are relying that each file inside a dataset will hold all possible histograms for this combination
    # That is, we do not support multiple DQMIO files containing the same (dataset_id, run_number, ls_number) information
    # Example:
    # File_id 123 on dataset_id 1 -> contains 5 1d-histograms for the run_number 1 and ls_number 1
    # File_id 124 on dataset_id 1 -> contains 2 1d-histograms for the run_number 1 and ls_number 1
    #
    # if this step fails, you should manually check if this situation occurred or another bug happened
    # - if this situation occurred: we'll need to figured out how to generalize this table to satisfy this condition
    # - if another bug happened: remember to clean TH1 and TH2 histograms and subtract their respective count in MEs table before re-ingesting
    #
    # Note: the update_on_conflict argument is used to re-ingested successfully finished files to add different MEs not specified before in the etl.config
    update_on_conflict = last_status == StatusCollection.FINISHED
    transform_load_lumis(engine, reader, me_pattern, dataset_id, update_on_conflict)

    # This step will never fail regarding conflicting data, because we update the ls_count in each iteration
    # But, beware that this step should never run more than once for the same file
    # otherwise we'll end up with an incorrect ls_count for the run
    if last_status != StatusCollection.FINISHED:
        transform_load_run(engine, reader, dataset_id)

    # Close the reader and the root file
    reader.close()
