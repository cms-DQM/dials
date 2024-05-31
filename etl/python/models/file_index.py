import sqlalchemy as sa
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class StatusCollection:
    PENDING = "PENDING"
    DOWNLOAD_STARTED = "DOWNLOAD_STARTED"
    DOWNLOAD_ERROR = "DOWNLOAD_ERROR"
    DOWNLOAD_FILE_NOT_AVAILABLE = "DOWNLOAD_FILE_NOT_AVAILABLE"
    DOWNLOAD_FINISHED = "DOWNLOAD_FINISHED"
    INGESTION_STARTED = "INGESTION_STARTED"
    INGESTION_COPY_ERROR = "INGESTION_COPY_ERROR"
    INGESTION_ROOTFILE_ERROR = "INGESTION_ROOTFILE_ERROR"
    INGESTION_PARSING_ERROR = "INGESTION_PARSING_ERROR"
    FINISHED = "FINISHED"


class FactFileIndex(Base):
    __tablename__ = "fact_file_index"

    dataset_id = sa.Column("dataset_id", sa.BigInteger)
    file_id = sa.Column("file_id", sa.BigInteger)
    file_size = sa.Column("file_size", sa.BigInteger)
    creation_date = sa.Column("creation_date", sa.DateTime)
    last_modification_date = sa.Column("last_modification_date", sa.DateTime)
    logical_file_name = sa.Column("logical_file_name", sa.String(length=255))
    status = sa.Column("status", sa.String(length=255))
    err_trace = sa.Column("err_trace", sa.String(length=2295), nullable=True)

    __table_args__ = (
        sa.PrimaryKeyConstraint("dataset_id", "file_id"),
        sa.Index("idx_fdi_logical_file_name", "logical_file_name"),
        sa.Index("idx_fdi_status", "status"),
    )
