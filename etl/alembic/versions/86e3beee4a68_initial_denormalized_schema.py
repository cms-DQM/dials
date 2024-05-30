# noqa: INP001

"""initial denormalized schema

Revision ID: 86e3beee4a68
Revises:
Create Date: 2024-03-26 16:09:50.366283

"""

from collections.abc import Sequence

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "86e3beee4a68"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


# All data marts have the same modeling schema
# so we define all schemas generically
# and call the from each upgrade/downgrade function
def dim_monitoring_elements() -> list:
    op.execute("""
    CREATE TABLE IF NOT EXISTS dim_monitoring_elements (
        me_id SERIAL,
        me VARCHAR(255),
        count INT,
        dim INT,
        CONSTRAINT dim_monitoring_elements_pk PRIMARY KEY (me_id),
        CONSTRAINT unique_me UNIQUE (me)
    );
    """)


def fact_dataset_index() -> list:
    op.execute("""
    CREATE TABLE IF NOT EXISTS fact_dataset_index (
        dataset_id BIGINT,
        dataset VARCHAR(255),
        era VARCHAR(255),
        data_tier VARCHAR(255),
        primary_ds_name VARCHAR(255),
        processed_ds_name VARCHAR(255),
        processing_version INT,
        last_modification_date TIMESTAMP WITHOUT TIME ZONE,
        CONSTRAINT fact_dataset_index_pk PRIMARY KEY (dataset_id)
    );
    """)
    op.execute("CREATE INDEX idx_fdi_dataset ON fact_dataset_index (dataset);")
    op.execute("CREATE INDEX idx_fdi_era ON fact_dataset_index (era);")
    op.execute("""
    CREATE OR REPLACE FUNCTION create_partition(table_name TEXT, partition_name TEXT, partition_values BIGINT) RETURNS void AS $$
    BEGIN
        EXECUTE format(
            'CREATE TABLE IF NOT EXISTS %I PARTITION OF %I FOR VALUES IN (%L);',
            partition_name, table_name, partition_values
        );
    END;
    $$ LANGUAGE plpgsql;
    """)


def fact_file_index() -> list:
    op.execute("""
    CREATE TABLE IF NOT EXISTS fact_file_index (
        dataset_id BIGINT,
        file_id BIGINT,
        file_size BIGINT,
        creation_date TIMESTAMP WITHOUT TIME ZONE,
        last_modification_date TIMESTAMP WITHOUT TIME ZONE,
        logical_file_name VARCHAR(255),
        status VARCHAR(255),
        err_trace VARCHAR(2295),
        CONSTRAINT fact_file_index_pk PRIMARY KEY (dataset_id, file_id)
    ) PARTITION BY LIST (dataset_id);
    """)
    op.execute("CREATE INDEX idx_ffi_file_id ON fact_file_index (file_id);")
    op.execute("CREATE INDEX idx_ffi_logical_file_name ON fact_file_index (logical_file_name);")
    op.execute("CREATE INDEX idx_ffi_status ON fact_file_index (status);")


def fact_run() -> list:
    op.execute("""
    CREATE TABLE IF NOT EXISTS fact_run (
        dataset_id BIGINT,
        run_number INT,
        ls_count INT,
        CONSTRAINT fact_run_pk PRIMARY KEY (dataset_id, run_number)
    ) PARTITION BY LIST (dataset_id)
    """)
    op.execute("CREATE INDEX idx_fr_run_number ON fact_run (run_number);")


def fact_lumisection() -> list:
    op.execute("""
    CREATE TABLE IF NOT EXISTS fact_lumisection (
        dataset_id BIGINT,
        run_number INT,
        ls_number INT,
        th1_count INT,
        th2_count INT,
        CONSTRAINT fact_lumisection_pk PRIMARY KEY (dataset_id, run_number, ls_number)
    ) PARTITION BY LIST (dataset_id);
    """)
    op.execute("CREATE INDEX idx_fl_run_number ON fact_lumisection (run_number);")
    op.execute("CREATE INDEX idx_fl_ls_number ON fact_lumisection (ls_number);")


def fact_th1() -> list:
    op.execute("""
    CREATE TABLE IF NOT EXISTS fact_th1 (
        dataset_id BIGINT,
        file_id BIGINT,
        run_number INT,
        ls_number INT,
        me_id INT,
        x_min DOUBLE PRECISION,
        x_max DOUBLE PRECISION,
        x_bin DOUBLE PRECISION,
        entries INT,
        data DOUBLE PRECISION[],
        CONSTRAINT fact_th1_pk PRIMARY KEY (dataset_id, run_number, ls_number, me_id)
    ) PARTITION BY LIST (dataset_id);
    """)
    op.execute("CREATE INDEX idx_th1_file_id ON fact_th1 (file_id);")
    op.execute("CREATE INDEX idx_th1_run_number ON fact_th1 (run_number);")
    op.execute("CREATE INDEX idx_th1_ls_number ON fact_th1 (ls_number);")
    op.execute("CREATE INDEX idx_th1_me_id ON fact_th1 (me_id);")
    op.execute("CREATE INDEX idx_th1_run_number_me_id ON fact_th1 (run_number, me_id);")


def fact_th2() -> list:
    """
    Note that "data" column is a 2D array, but from PG docs:

    The current implementation does not enforce the declared number of dimensions either.
    Arrays of a particular element type are all considered to be of the same type,
    regardless of size or number of dimensions. So, declaring the array size or number of
    dimensions in CREATE TABLE is simply documentation; it does not affect run-time behavior.
    # Source: https://www.postgresql.org/docs/current/arrays.html
    """
    op.execute("""
    CREATE TABLE IF NOT EXISTS fact_th2 (
        dataset_id BIGINT,
        file_id BIGINT,
        run_number INT,
        ls_number INT,
        me_id INT,
        x_min DOUBLE PRECISION,
        x_max DOUBLE PRECISION,
        x_bin DOUBLE PRECISION,
        y_min DOUBLE PRECISION,
        y_max DOUBLE PRECISION,
        y_bin DOUBLE PRECISION,
        entries INT,
        data DOUBLE PRECISION[],
        CONSTRAINT fact_th2_pk PRIMARY KEY (dataset_id, run_number, ls_number, me_id)
    ) PARTITION BY LIST (dataset_id);
    """)
    op.execute("CREATE INDEX idx_th2_file_id ON fact_th2 (file_id);")
    op.execute("CREATE INDEX idx_th2_run_number ON fact_th2 (run_number);")
    op.execute("CREATE INDEX idx_th2_ls_number ON fact_th2 (ls_number);")
    op.execute("CREATE INDEX idx_th2_me_id ON fact_th2 (me_id);")
    op.execute("CREATE INDEX idx_th2_run_number_me_id ON fact_th2 (run_number, me_id);")


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
    for run_table_migrations in tables_functions:
        run_table_migrations()


def delete_tables() -> None:
    for table_func in tables_functions:
        op.drop_table(table_func.__name__)
    op.execute("DROP FUNCTION create_partition(TEXT, TEXT, BIGINT)")


def upgrade(engine_name: str) -> None:
    # We don't need to create a function for each engine
    # if they are going to run the same code
    # By default alembic will execute the upgrade function for each engine separatedly
    # globals()["upgrade_%s" % engine_name]()
    create_tables()


def downgrade(engine_name: str) -> None:
    # Just like the upgrade function, we don't need a specific
    # downgrade function for each engine
    # globals()["downgrade_%s" % engine_name]()
    delete_tables()
