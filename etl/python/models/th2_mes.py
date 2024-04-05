import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

from .th2 import TH2


Base = declarative_base()


class TH2Mes(Base):
    __tablename__ = f"{TH2.__tablename__}_mes"

    title = sa.Column("title", sa.String(length=255))
    count = sa.Column("count", sa.BigInteger)

    __table_args__ = (sa.PrimaryKeyConstraint("title"),)
