from sqlalchemy.engine.base import Engine
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker

from ...models import DimMonitoringElements, FactTH1, FactTH2


def extract_me(engine: Engine, me: str):
    sess = sessionmaker(bind=engine)
    with sess() as session:
        query = session.query(DimMonitoringElements).filter(DimMonitoringElements.me == me)
        try:
            result = query.one()
        except NoResultFound:
            result = None
        return result


def extract(engine: Engine, th_class: FactTH1 | FactTH2, dataset_id: int, file_id: int, me_id: int):
    sess = sessionmaker(bind=engine)
    with sess() as session:
        query = session.query(th_class).filter(
            th_class.dataset_id == dataset_id,
            th_class.file_id == file_id,
            th_class.me_id == me_id,
        )
        return query.all()
