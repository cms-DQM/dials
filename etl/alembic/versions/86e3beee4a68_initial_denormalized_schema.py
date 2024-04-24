# noqa: INP001

"""initial denormalized schema

Revision ID: 86e3beee4a68
Revises:
Create Date: 2024-03-26 16:09:50.366283

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "86e3beee4a68"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade(engine_name: str) -> None:
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name: str) -> None:
    globals()["downgrade_%s" % engine_name]()


# All data marts have the same modeling schema
# so we define all schemas generically
# and call the from each upgrade/downgrade function
def dim_monitoring_elements() -> list:
    return {
        "table_name": "dim_monitoring_elements",
        "columns": [
            sa.Column("me_id", sa.BigInteger, autoincrement=True),
            sa.Column("me", sa.String(length=255)),
            sa.Column("count", sa.Integer),
            sa.Column("dim", sa.Integer),
            sa.PrimaryKeyConstraint("me_id"),
            sa.Index("idx_me", "me"),
            sa.UniqueConstraint("me", name="unique_me"),
        ],
    }


def fact_dataset_index() -> list:
    return {
        "table_name": "fact_dataset_index",
        "columns": [
            sa.Column("dataset_id", sa.BigInteger),
            sa.Column("dataset", sa.String(length=255)),
            sa.Column("era", sa.String(length=255)),
            sa.Column("data_tier", sa.String(length=255)),
            sa.Column("primary_ds_name", sa.String(length=255)),
            sa.Column("processed_ds_name", sa.String(length=255)),
            sa.Column("processing_version", sa.Integer),
            sa.Column("last_modification_date", sa.DateTime),
            sa.PrimaryKeyConstraint("dataset_id"),
            sa.Index("idx_dataset", "dataset"),
            sa.Index("idx_era", "era"),
        ],
    }


def fact_file_index() -> list:
    return {
        "table_name": "fact_file_index",
        "columns": [
            sa.Column("file_id", sa.BigInteger),
            sa.Column("dataset_id", sa.BigInteger),
            sa.Column("file_size", sa.BigInteger),
            sa.Column("creation_date", sa.DateTime),
            sa.Column("last_modification_date", sa.DateTime),
            sa.Column("logical_file_name", sa.String(length=255)),
            sa.Column("status", sa.String(length=255)),
            sa.Column("err_trace", sa.String(length=2295), nullable=True),
            sa.PrimaryKeyConstraint("file_id"),
            sa.Index("idx_fdi_dataset_id", "dataset_id"),
            sa.Index("idx_fdi_logical_file_name", "logical_file_name"),
            sa.Index("idx_fdi_status", "status"),
        ],
    }


def fact_run() -> list:
    return {
        "table_name": "fact_run",
        "columns": [
            sa.Column("run_number", sa.Integer),
            sa.Column("dataset_id", sa.BigInteger),
            sa.Column("ls_count", sa.Integer),
            sa.PrimaryKeyConstraint("run_number", "dataset_id"),
            sa.Index("idx_fr_dataset_id", "dataset_id"),
            sa.Index("idx_fr_run_number", "run_number"),
        ],
    }


def fact_lumisection() -> list:
    return {
        "table_name": "fact_lumisection",
        "columns": [
            sa.Column("dataset_id", sa.BigInteger),
            sa.Column("run_number", sa.Integer),
            sa.Column("ls_number", sa.Integer),
            sa.Column("ls_id", sa.BigInteger),
            sa.Column("th1_count", sa.Integer),
            sa.Column("th2_count", sa.Integer),
            sa.PrimaryKeyConstraint("dataset_id", "run_number", "ls_number"),
            sa.Index("idx_fls_ls_id", "ls_id"),
            sa.Index("idx_fls_dataset_id", "dataset_id"),
            sa.Index("idx_fls_run_number", "run_number"),
            sa.Index("idx_fls_ls_number", "ls_number"),
        ],
    }


def fact_th1() -> list:
    return {
        "table_name": "fact_th1",
        "columns": [
            sa.Column("hist_id", sa.BigInteger, autoincrement=True),
            sa.Column("file_id", sa.BigInteger),
            sa.Column("dataset_id", sa.BigInteger),
            sa.Column("me_id", sa.Integer),
            sa.Column("ls_id", sa.BigInteger),
            sa.Column("run_number", sa.Integer),
            sa.Column("ls_number", sa.Integer),
            sa.Column("x_min", sa.Float),
            sa.Column("x_max", sa.Float),
            sa.Column("x_bin", sa.Float),
            sa.Column("entries", sa.Integer),
            sa.Column("data", sa.ARRAY(sa.Float)),
            sa.PrimaryKeyConstraint("hist_id"),
            sa.Index("idx_th1_file_id", "file_id"),
            sa.Index("idx_th1_dataset_id", "dataset_id"),
            sa.Index("idx_th1_ls_id", "ls_id"),
            sa.Index("idx_th1_me_id", "me_id"),
            sa.Index("idx_th1_run_number", "run_number"),
            sa.Index("idx_th1_ls_number", "ls_number"),
        ],
    }


def fact_th2() -> list:
    """
    Note that "data" column is a 2D array, but from PG docs:

    The current implementation does not enforce the declared number of dimensions either.
    Arrays of a particular element type are all considered to be of the same type,
    regardless of size or number of dimensions. So, declaring the array size or number of
    dimensions in CREATE TABLE is simply documentation; it does not affect run-time behavior.
    # Source: https://www.postgresql.org/docs/current/arrays.html
    """
    return {
        "table_name": "fact_th2",
        "columns": [
            sa.Column("hist_id", sa.BigInteger, autoincrement=True),
            sa.Column("file_id", sa.BigInteger),
            sa.Column("dataset_id", sa.BigInteger),
            sa.Column("me_id", sa.Integer),
            sa.Column("ls_id", sa.BigInteger),
            sa.Column("run_number", sa.Integer),
            sa.Column("ls_number", sa.Integer),
            sa.Column("x_min", sa.Float),
            sa.Column("x_max", sa.Float),
            sa.Column("x_bin", sa.Float),
            sa.Column("y_min", sa.Float),
            sa.Column("y_max", sa.Float),
            sa.Column("y_bin", sa.Float),
            sa.Column("entries", sa.Integer),
            sa.Column("data", sa.ARRAY(sa.Float)),
            sa.PrimaryKeyConstraint("hist_id"),
            sa.Index("idx_th2_file_id", "file_id"),
            sa.Index("idx_th2_dataset_id", "dataset_id"),
            sa.Index("idx_th2_me_id", "me_id"),
            sa.Index("idx_th2_ls_id", "ls_id"),
            sa.Index("idx_th2_run_number", "run_number"),
            sa.Index("idx_th2_ls_number", "ls_number"),
        ],
    }


tables_functions = [
    dim_monitoring_elements,
    fact_dataset_index,
    fact_file_index,
    fact_run,
    fact_lumisection,
    fact_th1,
    fact_th2,
]


def create_tables() -> None:
    for table_func in tables_functions:
        schema = table_func()
        op.create_table(schema["table_name"], *schema["columns"])


def delete_tables() -> None:
    for table_func in tables_functions:
        schema = table_func()
        op.drop_table(schema["table_name"])


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
