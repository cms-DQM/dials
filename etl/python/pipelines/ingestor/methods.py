import os
import os.path
import traceback
from functools import reduce

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker

from ...common.dqmio_reader import DQMIOReader
from ...common.lxplus_client import MinimalLXPlusClient
from ...common.pgsql import copy_expert, copy_expert_onconflict_skip
from ...config import th1_types, th2_types
from ...env import conn_str, files_landing_dir
from ...models import TH1, TH2, DQMIOIndex, Lumisection, Run
from ...models.dqmio_index import StatusCollection


CHUNK_SIZE = 10000


def pre_extract(engine: Engine, file_id: int) -> str:
    session = sessionmaker(bind=engine)
    with session() as sess:
        row = sess.query(DQMIOIndex).filter_by(file_id=file_id).first()
        row.status = StatusCollection.STARTED
        sess.commit()
        return row.logical_file_name


# TODO: Instead of ssh-ing directly we can check if the file exists if EOS is mounted locally
# TODO: Instead of listing the directory, we can check if the file exists
# TODO: We should also check if the file is not corrupted
def extract(logical_file_name: str) -> str:
    with MinimalLXPlusClient() as client:
        downloaded_files = client.ls(files_landing_dir)
        fname = logical_file_name.replace("/", "_")[1:]

        if fname not in downloaded_files:
            client.init_proxy()
            client.xrdcp(logical_file_name, files_landing_dir)

        remote_fpath = os.path.join(files_landing_dir, fname)
        local_fpath = client.scp_to_tmp(remote_fpath)
        return local_fpath


# TODO: Instead of ignoring on conflict
# we should update the ls_count field for the run if it already exists
# since a run can be divided in many files, but the lumisections are unique across then
def transform_load_run(engine: Engine, reader: DQMIOReader) -> None:
    run_lumi = reader.index_keys
    runs = reduce(lambda acc, cur: {cur[0]: acc.get(cur[0], 0) + 1}, run_lumi, {})
    runs = [{"run_number": run, "ls_count": ls_count} for run, ls_count in runs.items()]

    runs = pd.DataFrame(runs)
    runs.to_sql(
        name=Run.__tablename__,
        con=engine,
        if_exists="append",
        index=False,
        chunksize=CHUNK_SIZE,
        method=copy_expert_onconflict_skip,
    )


def transform_load_lumis(engine: Engine, reader: DQMIOReader, me_pattern: str) -> None:
    run_lumi = reader.index_keys

    lumis = []
    for run, lumi, ls_id in run_lumi:
        th1_me = reader.get_mes_for_lumi(run, lumi, types=th1_types, re_pattern=me_pattern)
        th2_me = reader.get_mes_for_lumi(run, lumi, types=th2_types, re_pattern=me_pattern)
        lumis.append({"ls_id": ls_id, "ls_number": lumi, "th1_count": len(th1_me), "th2_count": len(th2_me)})

    lumis = pd.DataFrame(lumis)
    lumis.to_sql(
        name=Lumisection.__tablename__,
        con=engine,
        if_exists="append",
        index=False,
        chunksize=CHUNK_SIZE,
        method=copy_expert,
    )


def transform_load_th(th_table: str, engine: Engine, reader: DQMIOReader, me_pattern: str, file_id: int) -> None:
    types = th1_types if th_table == "th1" else th2_types
    reader_func = reader.th1_from_cppyy if th_table == "th1" else reader.th2_from_cppyy
    run_lumi = reader.index_keys

    th_list = []
    chunk_count = 0
    for run, lumi, ls_id in run_lumi:
        me_list = reader.get_mes_for_lumi(run, lumi, types=types, re_pattern=me_pattern)
        for me in me_list:
            th_list.append({"file_id": file_id, "run_number": run, "ls_id": ls_id, **reader_func(me)})
            chunk_count += 1
            if chunk_count == CHUNK_SIZE:
                th_list = pd.DataFrame(th_list)
                th_list["data"] = th_list.data.apply(
                    lambda x: str(x).replace("[", "{").replace("]", "}").replace(" ", "")
                )
                th_list.to_sql(
                    name=th_table,
                    con=engine,
                    if_exists="append",
                    index=False,
                    method=copy_expert,
                )
                th_list = []
                chunk_count = 0

    if len(th_list) > 0:
        th_list = pd.DataFrame(th_list)
        th_list["data"] = th_list.data.apply(lambda x: str(x).replace("[", "{").replace("]", "}").replace(" ", ""))
        th_list.to_sql(
            name=th_table,
            con=engine,
            if_exists="append",
            index=False,
            method=copy_expert,
        )


def transform_load(engine: Engine, me_pattern: str, file_id: int, fpath: str) -> pd.DataFrame:
    reader = DQMIOReader(fpath)
    transform_load_run(engine, reader)
    transform_load_lumis(engine, reader, me_pattern)
    transform_load_th(TH1.__tablename__, engine, reader, me_pattern, file_id)
    transform_load_th(TH2.__tablename__, engine, reader, me_pattern, file_id)


def post_load(engine: Engine, file_id: int) -> None:
    session = sessionmaker(bind=engine)
    with session() as sess:
        sess.query(DQMIOIndex).filter_by(file_id=file_id).update({"status": StatusCollection.FINISHED})
        sess.commit()


def error_handler(engine: Engine, file_id: int, err_trace: str) -> None:
    session = sessionmaker(bind=engine)
    with session() as sess:
        sess.query(DQMIOIndex).filter_by(file_id=file_id).update(
            {"status": StatusCollection.FAILED, "err_trace": err_trace}
        )
        sess.commit()


def clean_file(fpath: str) -> None:
    if os.path.isfile(fpath):
        os.unlink(fpath)
        os.rmdir(os.path.dirname(fpath))


def pipeline(workspace_name: str, workspace_mes: str, file_id: int):
    me_pattern = f"({'|'.join(workspace_mes)}).*"
    engine = create_engine(f"{conn_str}/{workspace_name}")
    logical_file_name = pre_extract(engine, file_id)

    try:
        fpath = extract(logical_file_name)
        transform_load(engine, me_pattern, file_id, fpath)
    except Exception as e:
        clean_file(fpath)
        err_trace = traceback.format_exc()
        error_handler(engine, file_id, err_trace)
        raise e  # We are raising to mark the task as failed in celery broker
    else:
        clean_file(fpath)
        post_load(engine, file_id)
