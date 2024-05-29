import sqlalchemy as sa
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class FactTH1(Base):
    __tablename__ = "fact_th1"

    dataset_id = sa.Column("dataset_id", sa.BigInteger)
    file_id = sa.Column("file_id", sa.BigInteger)
    run_number = sa.Column("run_number", sa.Integer)
    ls_number = sa.Column("ls_number", sa.Integer)
    me_id = sa.Column("me_id", sa.Integer)
    x_min = sa.Column("x_min", sa.Float)
    x_max = sa.Column("x_max", sa.Float)
    x_bin = sa.Column("x_bin", sa.Float)
    entries = sa.Column("entries", sa.Integer)
    data = sa.Column("data", sa.ARRAY(sa.Float))

    __table_args__ = (
        sa.PrimaryKeyConstraint("dataset_id", "run_number", "ls_number", "me_id"),
        sa.Index("idx_th1_file_id", "file_id"),
        sa.Index("idx_th1_run_number", "run_number"),
        sa.Index("idx_th1_ls_number", "ls_number"),
        sa.Index("idx_th1_me_id", "me_id"),
        sa.Index("idx_th1_run_number_me_id", "run_number", "me_id"),
    )
