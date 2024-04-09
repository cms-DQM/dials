import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class StatusCollection:
    INDEXED = "INDEXED"
    PENDING = "PENDING"
    STARTED = "STARTED"
    DOWNLOAD_ERROR = "DOWNLOAD_ERROR"
    PARSING_ERROR = "PARSING_ERROR"
    FINISHED = "FINISHED"


# Fact constellation schema
# ........................
class DQMIOIndex(Base):
    __tablename__ = "dqmio_index"

    file_id = sa.Column("file_id", sa.BigInteger)
    file_size = sa.Column("file_size", sa.BigInteger)
    era = sa.Column("era", sa.String(length=5))
    campaign = sa.Column("campaign", sa.String(length=15))
    primary_dataset = sa.Column("primary_dataset", sa.String(length=15))
    creation_date = sa.Column("creation_date", sa.DateTime)
    last_modification_date = sa.Column("last_modification_date", sa.DateTime)
    logical_file_name = sa.Column("logical_file_name", sa.String(length=255))
    status = sa.Column("status", sa.String(length=15))
    err_trace = sa.Column("err_trace", sa.String(length=5000), nullable=True)

    __table_args__ = (
        sa.PrimaryKeyConstraint("file_id"),
        sa.Index("idx_file_size", "file_size"),
        sa.Index("idx_era", "era"),
        sa.Index("idx_campaign", "campaign"),
        sa.Index("idx_primary_dataset", "primary_dataset"),
        sa.Index("idx_logical_file_name", "logical_file_name"),
        sa.Index("idx_status", "status"),
    )
