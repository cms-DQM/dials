import ROOT
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker

from ...models import DimMLModelsIndex


def validate_root_file(fpath: str) -> None:
    """
    Opening the ROOT file and getting the UUID seems to be enough
    to check fi the file is corrupted or not.
    """
    with ROOT.TFile(fpath) as root_file:
        root_file.GetUUID().AsString()


def fetch_active_models(engine: Engine) -> list[DimMLModelsIndex]:
    Session = sessionmaker(bind=engine)  # noqa: N806
    with Session() as session:
        return session.query(DimMLModelsIndex).filter(DimMLModelsIndex.active).all()
