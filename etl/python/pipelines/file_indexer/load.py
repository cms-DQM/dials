from functools import partial

import pandas as pd
from sqlalchemy.engine.base import Engine
from sqlalchemy.inspection import inspect

from ...common.pgsql import copy_expert_onconflict_skip
from ...config import common_chunk_size
from ...models import FactFileIndex


def load(engine: Engine, file_index: pd.DataFrame) -> list:
    pk_name = inspect(FactFileIndex).primary_key[0].name
    method = partial(copy_expert_onconflict_skip, return_ids=True, pk=pk_name)
    return file_index.to_sql(
        name=FactFileIndex.__tablename__,
        con=engine,
        if_exists="append",
        index=False,
        chunksize=common_chunk_size,
        method=method,
    )
