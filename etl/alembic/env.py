# ruff: noqa: INP001

import json
import logging
import re
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, engine_from_config, exc, pool, text


USE_TWOPHASE = False

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")

# gather section names referring to different
# databases.  These are named "engine1", "engine2"
# in the sample .ini file.
db_names = config.get_main_option("databases", "")

# overwrite alembic-init db urls from the config file
try:
    with open("./alembic.env.json") as fd:
        settings: dict = json.load(fd)
except FileNotFoundError:
    logger.warning("alembic.env.json not found - use default alembic.ini configuration")
except Exception as err:  # noqa: BLE001
    msg = f"Failed to load alembic.env.json - {err}"
    logger.warning(msg)
    quit()
else:
    for engine, conn_str in settings.items():
        config.set_section_option(engine, "sqlalchemy.url", conn_str)

# add your model's MetaData objects here
# for 'autogenerate' support.  These must be set
# up to hold just those tables targeting a
# particular database. table.tometadata() may be
# helpful here in case a "copy" of
# a MetaData is needed.
# from myapp import mymodel
# target_metadata = {
#       'engine1':mymodel.metadata1,
#       'engine2':mymodel.metadata2
# }
target_metadata = {}

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def create_db_if_not_exists(db_uri):
    database = db_uri.split("/")[-1]
    db_postgres = "/".join(db_uri.split("/")[0:-1]) + "/postgres"
    try:
        engine = create_engine(db_uri)
        with engine.connect() as conn:
            pass
            print(f"Database {database} already exists.")
    except exc.OperationalError:
        msg = f"Database {database} does not exist. Creating now."
        logger.warning(msg)
        engine = create_engine(db_postgres)
        with engine.connect() as conn:
            conn.execute(text("commit"))
            conn.execute(text(f"CREATE DATABASE {database};"))


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # for the --sql use case, run migrations for each URL into
    # individual files.

    engines = {}
    for name in re.split(r",\s*", db_names):
        db_uri = context.config.get_section_option(name, "sqlalchemy.url")
        create_db_if_not_exists(db_uri)

        engines[name] = rec = {}
        rec["url"] = db_uri

    for name, rec in engines.items():
        msg = f"Running migrations for database {name}..."
        logger.info(msg)
        file_ = f"{name}.sql"
        msg = f"Writing output to {file_}"
        logger.info(msg)
        with open(file_, "w") as buffer:
            context.configure(
                url=rec["url"],
                output_buffer=buffer,
                target_metadata=target_metadata.get(name),
                literal_binds=True,
                dialect_opts={"paramstyle": "named"},
            )
            with context.begin_transaction():
                context.run_migrations(engine_name=name)


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    # for the direct-to-DB use case, start a transaction on all
    # engines, then run all migrations, then commit all transactions.

    engines = {}
    for name in re.split(r",\s*", db_names):
        db_uri = context.config.get_section_option(name, "sqlalchemy.url")
        create_db_if_not_exists(db_uri)

        engines[name] = rec = {}
        rec["engine"] = engine_from_config(
            context.config.get_section(name, {}),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

    for _, rec in engines.items():
        engine = rec["engine"]
        rec["connection"] = conn = engine.connect()

        if USE_TWOPHASE:
            rec["transaction"] = conn.begin_twophase()
        else:
            rec["transaction"] = conn.begin()

    try:
        for name, rec in engines.items():
            msg = f"Running migrations for database {name}..."
            logger.info(msg)
            context.configure(
                connection=rec["connection"],
                upgrade_token="%s_upgrades" % name,
                downgrade_token="%s_downgrades" % name,
                target_metadata=target_metadata.get(name),
            )
            context.run_migrations(engine_name=name)

        if USE_TWOPHASE:
            for rec in engines.values():
                rec["transaction"].prepare()

        for rec in engines.values():
            rec["transaction"].commit()
    except:
        for rec in engines.values():
            rec["transaction"].rollback()
        raise
    finally:
        for rec in engines.values():
            rec["connection"].close()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
