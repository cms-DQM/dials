# noqa: INP001

"""add ml bad lumis

Revision ID: bb3f9a1b3fa2
Revises: 86e3beee4a68
Create Date: 2024-03-26 16:09:50.366283

"""

from collections.abc import Sequence

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "bb3f9a1b3fa2"
down_revision: str = "86e3beee4a68"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def fact_ml_bad_lumis() -> list:
    # We don't need extra indexes
    op.execute("""
    CREATE TABLE IF NOT EXISTS fact_ml_bad_lumis (
        model_id BIGINT,
        dataset_id BIGINT,
        file_id BIGINT,
        run_number INT,
        ls_number INT,
        me_id INT,
        mse DOUBLE PRECISION,
        CONSTRAINT fact_ml_bad_lumis_pk PRIMARY KEY (model_id, dataset_id, run_number, ls_number, me_id)
    );
    """)
    op.execute("CREATE INDEX idx_mlbl_dataset_id_run_number ON fact_ml_bad_lumis (dataset_id, run_number);")


def dim_ml_models_index() -> list:
    op.execute("""
    CREATE TABLE IF NOT EXISTS dim_ml_models_index (
        model_id SERIAL,
        filename VARCHAR(255),
        target_me VARCHAR(255),
        active BOOLEAN,
        CONSTRAINT dim_ml_models_index_pk PRIMARY KEY (model_id)
    );
    """)
    op.execute("CREATE INDEX idx_active ON dim_ml_models_index (active);")


def upgrade(engine_name: str) -> None:
    dim_ml_models_index()
    fact_ml_bad_lumis()


def downgrade(engine_name: str) -> None:
    op.drop_table("dim_ml_models_index")
    op.drop_table("fact_ml_bad_lumis")
