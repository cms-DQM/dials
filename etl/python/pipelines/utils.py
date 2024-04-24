import os
import os.path

from sqlalchemy import inspect
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker

from ..models import FactFileIndex


def sqlachemy_asdict(obj) -> list:
    return [{k: v for k, v in elem.__dict__.items() if k != "_sa_instance_state"} for elem in obj]


def list_to_sql_array(arr: list) -> str:
    return str(arr).replace("[", "{").replace("]", "}").replace(" ", "")


def get_table_columns(base_class):
    return [c.key for c in inspect(base_class).mapper.column_attrs]


def clean_file(fpath: str) -> None:
    if os.path.isfile(fpath):
        os.unlink(fpath)
        os.rmdir(os.path.dirname(fpath))


def error_handler(engine: Engine, file_id: int, err_trace: str, status: str) -> None:
    session = sessionmaker(bind=engine)
    with session() as sess:
        sess.query(FactFileIndex).filter_by(file_id=file_id).update({"status": status, "err_trace": err_trace})
        sess.commit()
