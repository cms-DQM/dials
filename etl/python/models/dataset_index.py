import sqlalchemy as sa
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class FactDatasetIndex(Base):
    __tablename__ = "fact_dataset_index"

    dataset_id = sa.Column("dataset_id", sa.BigInteger)
    dataset = sa.Column("dataset", sa.String(length=255))
    era = sa.Column("era", sa.String(length=255))
    data_tier = sa.Column("data_tier", sa.String(length=255))
    primary_ds_name = sa.Column("primary_ds_name", sa.String(length=255))
    processed_ds_name = sa.Column("processed_ds_name", sa.String(length=255))
    processing_version = sa.Column("processing_version", sa.Integer)
    last_modification_date = sa.Column("last_modification_date", sa.DateTime)

    __table_args__ = (
        sa.PrimaryKeyConstraint("dataset_id"),
        sa.Index("idx_dataset", "dataset"),
        sa.Index("idx_era", "era"),
    )
