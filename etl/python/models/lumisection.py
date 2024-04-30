import sqlalchemy as sa
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class FactLumisection(Base):
    __tablename__ = "fact_lumisection"

    dataset_id = sa.Column("dataset_id", sa.BigInteger)
    run_number = sa.Column("run_number", sa.Integer)
    ls_number = sa.Column("ls_number", sa.Integer)
    th1_count = sa.Column("th1_count", sa.Integer)
    th2_count = sa.Column("th2_count", sa.Integer)

    __table_args__ = (
        sa.PrimaryKeyConstraint("dataset_id", "run_number", "ls_number"),
        sa.Index("idx_fls_dataset_id", "dataset_id"),
        sa.Index("idx_fls_run_number", "run_number"),
        sa.Index("idx_fls_ls_number", "ls_number"),
    )
