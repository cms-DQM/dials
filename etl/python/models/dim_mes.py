import sqlalchemy as sa
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class DimMonitoringElements(Base):
    __tablename__ = "dim_monitoring_elements"

    me_id = sa.Column("me_id", sa.BigInteger, autoincrement=True)
    me = sa.Column("me", sa.String(length=255))
    count = sa.Column("count", sa.Integer)
    dim = sa.Column("dim", sa.Integer)

    __table_args__ = (
        sa.PrimaryKeyConstraint("me_id"),
        sa.Index("idx_me", "me"),
        sa.UniqueConstraint("me", name="unique_me"),
    )
