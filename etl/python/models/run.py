import sqlalchemy as sa
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class FactRun(Base):
    __tablename__ = "fact_run"

    dataset_id = sa.Column("dataset_id", sa.BigInteger)
    run_number = sa.Column("run_number", sa.Integer)
    ls_count = sa.Column("ls_count", sa.Integer)

    __table_args__ = (
        sa.PrimaryKeyConstraint("dataset_id", "run_number"),
        sa.Index("idx_fr_run_number", "run_number"),
    )
