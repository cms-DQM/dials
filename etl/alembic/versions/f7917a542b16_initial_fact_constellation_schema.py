# ruff: noqa: INP001

"""initial fact constellation schema

Revision ID: f7917a542b16
Revises:
Create Date: 2024-03-26 16:18:04.051932

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "f7917a542b16"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade(engine_name: str) -> None:
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name: str) -> None:
    globals()["downgrade_%s" % engine_name]()


# All data marts have the same modeling schema
# so we define all schemas generically
# and call it from each upgrade function
def table_dqmio_index() -> list:
    return [
        sa.Column("file_id", sa.BigInteger),
        sa.Column("file_size", sa.BigInteger),
        sa.Column("era", sa.String(length=5)),
        sa.Column("campaign", sa.String(length=15)),
        sa.Column("dataset", sa.String(length=50)),
        sa.Column("creation_date", sa.DateTime),
        sa.Column("last_modification_date", sa.DateTime),
        sa.Column("logical_file_name", sa.String(length=255)),
        sa.Column("status", sa.String(length=15)),
        sa.Column("err_trace", sa.String(length=5000), nullable=True),
        sa.PrimaryKeyConstraint("file_id"),
        sa.Index("idx_file_size", "file_size"),
        sa.Index("idx_era", "era"),
        sa.Index("idx_campaign", "campaign"),
        sa.Index("idx_dataset", "dataset"),
        sa.Index("idx_logical_file_name", "logical_file_name"),
        sa.Index("idx_status", "status"),
    ]


def table_run() -> list:
    return [
        sa.Column("run_number", sa.Integer),
        sa.Column("ls_count", sa.Integer),
        sa.PrimaryKeyConstraint("run_number"),
    ]


def table_lumisection() -> list:
    return [
        sa.Column("ls_id", sa.BigInteger),
        sa.Column("ls_number", sa.Integer),
        sa.Column("th1_count", sa.Integer),
        sa.Column("th2_count", sa.Integer),
        sa.PrimaryKeyConstraint("ls_id"),
        sa.Index("idx_ls_number", "ls_number"),
    ]


def table_th1_mes() -> list:
    return [
        sa.Column("title", sa.String(length=255)),
        sa.Column("count", sa.BigInteger),
        sa.PrimaryKeyConstraint("title"),
    ]


def table_th1() -> list:
    return [
        sa.Column("hist_id", sa.BigInteger, autoincrement=True),
        sa.Column("file_id", sa.BigInteger),
        sa.Column("run_number", sa.BigInteger),
        sa.Column("ls_id", sa.BigInteger),
        sa.Column("title", sa.String(length=255)),
        sa.Column("x_min", sa.Float),
        sa.Column("x_max", sa.Float),
        sa.Column("x_bin", sa.Float),
        sa.Column("entries", sa.Integer),
        sa.Column("data", sa.ARRAY(sa.Float)),
        sa.PrimaryKeyConstraint("hist_id"),
        sa.ForeignKeyConstraint(["file_id"], ["dqmio_index.file_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["run_number"], ["run.run_number"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["ls_id"], ["lumisection.ls_id"], ondelete="CASCADE"),
        sa.Index("idx_th1_file_id", "file_id"),
        sa.Index("idx_th1_run_number", "run_number"),
        sa.Index("idx_th1_ls_id", "ls_id"),
        sa.Index("idx_th1_title", "title"),
        sa.Index("idx_th1_entries", "entries"),
    ]


def table_th2_mes() -> list:
    return [
        sa.Column("title", sa.String(length=255)),
        sa.Column("count", sa.BigInteger),
        sa.PrimaryKeyConstraint("title"),
    ]


def table_th2() -> list:
    """
    Note that "data" column is a 2D array, but from PG docs:

    The current implementation does not enforce the declared number of dimensions either.
    Arrays of a particular element type are all considered to be of the same type,
    regardless of size or number of dimensions. So, declaring the array size or number of
    dimensions in CREATE TABLE is simply documentation; it does not affect run-time behavior.
    # Source: https://www.postgresql.org/docs/current/arrays.html
    """
    return [
        sa.Column("hist_id", sa.BigInteger, autoincrement=True),
        sa.Column("file_id", sa.BigInteger),
        sa.Column("run_number", sa.BigInteger),
        sa.Column("ls_id", sa.BigInteger),
        sa.Column("title", sa.String(length=255)),
        sa.Column("x_min", sa.Float),
        sa.Column("x_max", sa.Float),
        sa.Column("x_bin", sa.Float),
        sa.Column("y_min", sa.Float),
        sa.Column("y_max", sa.Float),
        sa.Column("y_bin", sa.Float),
        sa.Column("entries", sa.Integer),
        sa.Column("data", sa.ARRAY(sa.Float)),
        sa.PrimaryKeyConstraint("hist_id"),
        sa.ForeignKeyConstraint(["file_id"], ["dqmio_index.file_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["run_number"], ["run.run_number"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["ls_id"], ["lumisection.ls_id"], ondelete="CASCADE"),
        sa.Index("idx_th2_file_id", "file_id"),
        sa.Index("idx_th2_run_number", "run_number"),
        sa.Index("idx_th2_ls_id", "ls_id"),
        sa.Index("idx_th2_title", "title"),
        sa.Index("idx_th2_entries", "entries"),
    ]


def create_tables() -> None:
    op.create_table("dqmio_index", *table_dqmio_index())
    op.create_table("run", *table_run())
    op.create_table("lumisection", *table_lumisection())
    op.create_table("th1_mes", *table_th1_mes())
    op.create_table("th1", *table_th1())
    op.create_table("th2_mes", *table_th2_mes())
    op.create_table("th2", *table_th2())


def delete_tables() -> None:
    op.drop_table("th2")
    op.drop_table("th2_mes")
    op.drop_table("th1")
    op.drop_table("th1_mes")
    op.drop_table("lumisection")
    op.drop_table("run")
    op.drop_table("dqmio_index")


def upgrade_csc() -> None:
    create_tables()


def upgrade_ecal() -> None:
    create_tables()


def upgrade_hcal() -> None:
    create_tables()


def upgrade_jetmet() -> None:
    create_tables()


def upgrade_tracker() -> None:
    create_tables()


def downgrade_csc() -> None:
    delete_tables()


def downgrade_ecal() -> None:
    delete_tables()


def downgrade_hcal() -> None:
    delete_tables()


def downgrade_jetmet() -> None:
    delete_tables()


def downgrade_tracker() -> None:
    delete_tables()
