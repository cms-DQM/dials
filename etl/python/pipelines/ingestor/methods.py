import os
import os.path
import shutil
import tempfile
import traceback
from functools import partial, reduce

import pandas as pd
import ROOT
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker

from ...common.dqmio_reader import DQMIOReader
from ...common.lxplus_client import MinimalLXPlusClient
from ...common.pgsql import copy_expert, copy_expert_onconflict_update
from ...config import th1_types, th2_types
from ...env import conn_str, eos_landing_zone, lxplus_pwd, lxplus_user, mounted_eos_path
from ...models import TH1, TH2, DQMIOIndex, Lumisection, Run
from ...models.dqmio_index import StatusCollection


CHUNK_SIZE = 10000


def clean_file(fpath: str) -> None:
    if os.path.isfile(fpath):
        os.unlink(fpath)
        os.rmdir(os.path.dirname(fpath))


def pre_extract(engine: Engine, file_id: int) -> str:
    session = sessionmaker(bind=engine)
    with session() as sess:
        row = sess.query(DQMIOIndex).filter_by(file_id=file_id).first()
        row.status = StatusCollection.STARTED
        sess.commit()
        return row.logical_file_name


def extract(workspace_name: str, logical_file_name: str) -> str:
    """
    Extracts a DQMIO file from EOS and returns the local path to the extracted file.
    If the file is corrupted (i.e. we cannot open it with ROOT), delete the file and raise the error.

    Logic:
    - If EOS is mounted locally we check if the file exists
        - If the file exists we copy it locally
        - Else we download it using xrdcp trough ssh and then copy it locally
    - Else we check if the file exists via ssh
        - If the file exists we copy it using scp
        - Else we download it using xrdcp and then copy it using scp

    TODO: The current solution download a file N times if it is used by multiple workspaces
          this was the fastest solution to implement to avoid the race condition

    - Solution 1:
    ------------------------------------------------------------------------------------------
    This is tricky to implement because we can't have indexer workers for each workspace
    since after the global indexer schedule the download job we need to know how many
    ingestor jobs the download job will schedule.
    ------------------------------------------------------------------------------------------
    Not download the same file to the same location simultaneously, i.e.
    we should add a new pipeline to out ETL workflow: Indexer -> Downloader -> Ingestor
    That is, after indexing each file we schedule download jobs and after finishing the download
    we schedule ingestion jobs for each workspace that would use that file (we should use one queue for each primary dataset).

    - Solution 2:
    ------------------------------------------------------------------------------------------
    This one was tested and it is not reliable multiple processes hanged
    during xrdcp execution and created the lock file simultaneously
    ------------------------------------------------------------------------------------------
    Another solution (this is faster) is to use a lock to make sure only one process can download
    the same file on the same location at the same time. That is, the process that won the race
    will generate a lock file to inform the other process that the file is being downloaded,
    and the processes that lost the race can ignore the xrdcp error and continuously check if the lock file exists.

    """
    fname = logical_file_name.replace("/", "_")[1:]
    tmp_dir = tempfile.mkdtemp()
    tmp_fpath = os.path.join(tmp_dir, fname)
    landing_path = os.path.join(eos_landing_zone, workspace_name)

    if mounted_eos_path:
        mounted_path = os.path.join(mounted_eos_path, workspace_name)
        does_dir_exists = os.path.isdir(mounted_path)
        if does_dir_exists is False:
            os.makedirs(mounted_path, exist_ok=True)

        mounted_fpath = os.path.join(mounted_path, fname)
        if not os.path.isfile(mounted_fpath):
            with MinimalLXPlusClient(lxplus_user, lxplus_pwd) as client:
                does_dir_exists = client.is_dir(landing_path)
                if does_dir_exists is False:
                    client.mkdir(landing_path)

                client.init_proxy()
                client.xrdcp(landing_path, logical_file_name)
        shutil.copy(mounted_fpath, tmp_fpath)
    else:
        landing_fpath = os.path.join(landing_path, fname)
        with MinimalLXPlusClient(lxplus_user, lxplus_pwd) as client:
            does_dir_exists = client.is_dir(landing_path)
            if does_dir_exists is False:
                client.mkdir(landing_path)

            is_file_available = client.is_file(landing_fpath)
            if is_file_available is False:
                client.init_proxy()
                client.xrdcp(landing_path, logical_file_name)
            client.scp(landing_fpath, tmp_fpath)

    # Checking if the file is corrupted
    try:
        with ROOT.TFile(tmp_fpath) as root_file:
            root_file.GetUUID().AsString()
    except Exception as err:
        clean_file(tmp_fpath)
        raise err  # Re-raise to the caller, we just captured to delete the leftover file

    return tmp_fpath


def transform_load_run(engine: Engine, reader: DQMIOReader) -> None:
    run_lumi = reader.index_keys
    runs = reduce(lambda acc, cur: {cur[0]: acc.get(cur[0], 0) + 1}, run_lumi, {})
    runs = [{"run_number": run, "ls_count": ls_count} for run, ls_count in runs.items()]
    expr = f"ls_count = {Run.__tablename__}.ls_count + EXCLUDED.ls_count"
    method = partial(copy_expert_onconflict_update, conflict_key="run_number", expr=expr)

    runs = pd.DataFrame(runs)
    runs.to_sql(
        name=Run.__tablename__,
        con=engine,
        if_exists="append",
        index=False,
        chunksize=CHUNK_SIZE,
        method=method,
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

    th_mes = {}
    th_list = []
    chunk_count = 0
    for run, lumi, ls_id in run_lumi:
        me_list = reader.get_mes_for_lumi(run, lumi, types=types, re_pattern=me_pattern)
        for me in me_list:
            th_entry = {"file_id": file_id, "run_number": run, "ls_id": ls_id, **reader_func(me)}
            th_list.append(th_entry)

            if th_entry.get("title") not in th_mes:
                th_mes[th_entry.get("title")] = 1
            else:
                th_mes[th_entry.get("title")] += 1

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

    expr = f"count = {th_table}_mes.count + EXCLUDED.count"
    method = partial(copy_expert_onconflict_update, conflict_key="title", expr=expr)
    th_mes = [{"title": title, "count": count} for title, count in th_mes.items()]
    th_mes = pd.DataFrame(th_mes)
    th_mes.to_sql(
        name=th_table + "_mes",
        con=engine,
        if_exists="append",
        index=False,
        method=method,
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


def error_handler(engine: Engine, file_id: int, err_trace: str, status: str) -> None:
    session = sessionmaker(bind=engine)
    with session() as sess:
        sess.query(DQMIOIndex).filter_by(file_id=file_id).update(
            {"status": StatusCollection.FAILED, "err_trace": err_trace}
        )
        sess.commit()


def pipeline(workspace_name: str, workspace_mes: str, file_id: int):
    me_pattern = f"({'|'.join(workspace_mes)}).*"
    engine = create_engine(f"{conn_str}/{workspace_name}")
    logical_file_name = pre_extract(engine, file_id)

    # If this fails, the function already cleans the leftover file
    # So we don't need to do it here (without knowing the generated tmp fpath)
    try:
        fpath = extract(workspace_name, logical_file_name)
    except Exception as e:
        err_trace = traceback.format_exc()
        error_handler(engine, file_id, err_trace, StatusCollection.DOWNLOAD_ERROR)
        raise e  # We are raising to mark the task as failed in celery broker

    # Since we know the fpath at this stage, we need to clean the file if it fails
    try:
        transform_load(engine, me_pattern, file_id, fpath)
    except Exception as e:
        clean_file(fpath)
        err_trace = traceback.format_exc()
        error_handler(engine, file_id, err_trace, StatusCollection.PARSING_ERROR)
        raise e  # We are raising to mark the task as failed in celery broker

    # If everything goes well, we can clean the file
    clean_file(fpath)
    post_load(engine, file_id)
