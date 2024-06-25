import sqlalchemy as sa
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class DimMLModelsIndex(Base):
    __tablename__ = "dim_ml_models_index"

    model_id = sa.Column("model_id", sa.BigInteger, autoincrement=True)
    filename = sa.Column("filename", sa.String(255))
    target_me = sa.Column("target_me", sa.String(255))
    thr = sa.Column("thr", sa.Float)
    active = sa.Column("active", sa.Boolean)

    __table_args__ = (
        sa.PrimaryKeyConstraint("model_id"),
        sa.Index("idx_active", "active"),
    )
