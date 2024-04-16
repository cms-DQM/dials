import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


# Fact constellation schema
# ........................
class Run(Base):
    __tablename__ = "run"

    run_number = sa.Column("run_number", sa.Integer)
    ls_count = sa.Column("ls_count", sa.Integer)

    __table_args__ = (sa.PrimaryKeyConstraint("run_number"),)
