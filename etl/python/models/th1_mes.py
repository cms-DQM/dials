import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

from .th1 import TH1


Base = declarative_base()


class TH1Mes(Base):
    __tablename__ = f"{TH1.__tablename__}_mes"

    title = sa.Column("title", sa.String(length=255))
    count = sa.Column("count", sa.BigInteger)

    __table_args__ = (sa.PrimaryKeyConstraint("title"),)
