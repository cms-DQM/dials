from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker

from ...models import FactFileIndex
from ...models.file_index import StatusCollection


def post_load(engine: Engine, file_id: int) -> None:
    session = sessionmaker(bind=engine)
    with session() as sess:
        sess.query(FactFileIndex).filter_by(file_id=file_id).update({"status": StatusCollection.FINISHED})
        sess.commit()
