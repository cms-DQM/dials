import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


# Fact constellation schema
# ........................
class Lumisection(Base):
    __tablename__ = "lumisection"

    ls_id = sa.Column("ls_id", sa.BigInteger)
    ls_number = sa.Column("ls_number", sa.Integer)
    th1_count = sa.Column("th1_count", sa.Integer)
    th2_count = sa.Column("th2_count", sa.Integer)

    __table_args__ = (
        sa.PrimaryKeyConstraint("ls_id"),
        sa.Index("idx_ls_number", "ls_number"),
    )
