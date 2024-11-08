from functools import partial

import pandas as pd
from sqlalchemy.engine.base import Engine
from sqlalchemy.inspection import inspect

from ...common.pgsql import copy_expert_onconflict_skip
from ...config import COMMON_CHUK_SIZE
from ...models import FactFileIndex


def load(engine: Engine, file_index: pd.DataFrame) -> list:
    pk_name = inspect(FactFileIndex).primary_key[1].name  # Be sure to select "file_id"
    method = partial(copy_expert_onconflict_skip, return_ids=True, pk=pk_name)
    return file_index.to_sql(
        name=FactFileIndex.__tablename__,
        con=engine,
        if_exists="append",
        index=False,
        chunksize=COMMON_CHUK_SIZE,
        method=method,
    )
