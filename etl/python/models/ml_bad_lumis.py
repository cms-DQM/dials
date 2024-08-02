import sqlalchemy as sa
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class FactMLBadLumis(Base):
    __tablename__ = "fact_ml_bad_lumis"

    model_id = sa.Column("model_id", sa.String(length=255))
    dataset_id = sa.Column("dataset_id", sa.BigInteger)
    file_id = sa.Column("file_id", sa.BigInteger)
    run_number = sa.Column("run_number", sa.Integer)
    ls_number = sa.Column("ls_number", sa.Integer)
    me_id = sa.Column("me_id", sa.Integer)
    mse = sa.Column("mse", sa.Float)

    __table_args__ = (
        sa.PrimaryKeyConstraint("model_id", "dataset_id", "run_number", "ls_number", "me_id"),
        sa.Index("idx_mlbl_dataset_id_run_number", "dataset_id", "run_number"),
    )
