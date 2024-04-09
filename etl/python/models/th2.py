import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

from .dqmio_index import DQMIOIndex
from .lumisection import Lumisection
from .run import Run


Base = declarative_base()


# Fact constellation schema
# ........................
class TH2(Base):
    __tablename__ = "th2"

    hist_id = sa.Column("hist_id", sa.BigInteger, autoincrement=True)
    file_id = sa.Column("file_id", sa.BigInteger)
    run_number = sa.Column("run_number", sa.BigInteger)
    ls_id = sa.Column("ls_id", sa.BigInteger)
    title = sa.Column("title", sa.String(length=255))
    x_min = sa.Column("x_min", sa.Float)
    x_max = sa.Column("x_max", sa.Float)
    x_bin = sa.Column("x_bin", sa.Integer)
    y_min = sa.Column("y_min", sa.Float)
    y_max = sa.Column("y_max", sa.Float)
    y_bin = sa.Column("y_bin", sa.Integer)
    entries = sa.Column("entries", sa.Integer)
    data = sa.Column("data", sa.ARRAY(sa.Float))

    __table_args__ = (
        sa.PrimaryKeyConstraint("hist_id"),
        sa.ForeignKeyConstraint(
            ["file_id"], [f"{DQMIOIndex.__tablename__}.{DQMIOIndex.file_id.name}"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["run_number"], [f"{Run.__tablename__}.{Run.run_number.name}"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["ls_id"], [f"{Lumisection.__tablename__}.{Lumisection.ls_id.name}"], ondelete="CASCADE"
        ),
        sa.Index("idx_th2_file_id", "file_id"),
        sa.Index("idx_th2_run_number", "run_number"),
        sa.Index("idx_th2_ls_id", "ls_id"),
        sa.Index("idx_th2_title", "title"),
        sa.Index("idx_th2_entries", "entries"),
    )
