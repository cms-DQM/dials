import sqlalchemy as sa
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class FactLumisection(Base):
    __tablename__ = "fact_lumisection"

    ls_id = sa.Column("ls_id", sa.BigInteger)
    dataset_id = sa.Column("dataset_id", sa.Integer)
    run_number = sa.Column("run_number", sa.Integer)
    ls_number = sa.Column("ls_number", sa.Integer)
    th1_count = sa.Column("th1_count", sa.Integer)
    th2_count = sa.Column("th2_count", sa.Integer)

    __table_args__ = (
        sa.PrimaryKeyConstraint("ls_id", "dataset_id"),
        sa.Index("idx_fls_ls_id", "ls_id"),
        sa.Index("idx_fls_dataset_id", "dataset_id"),
        sa.Index("idx_fls_run_number", "run_number"),
        sa.Index("idx_fls_ls_number", "ls_number"),
    )
