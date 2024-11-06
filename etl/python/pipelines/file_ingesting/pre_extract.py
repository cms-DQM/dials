from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker

from ...models import FactFileIndex
from ...models.file_index import StatusCollection


def pre_extract(engine: Engine, file_id: int) -> str:
    session = sessionmaker(bind=engine)
    with session() as sess:
        row = sess.query(FactFileIndex).filter_by(file_id=file_id).first()
        last_status = row.status
        row.status = StatusCollection.STARTED
        row.err_trace = None
        sess.commit()
        return row.logical_file_name, last_status
