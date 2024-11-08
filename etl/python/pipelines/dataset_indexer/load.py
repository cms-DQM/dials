from functools import partial

import pandas as pd
from sqlalchemy.engine.base import Engine
from sqlalchemy.inspection import inspect

from ...common.pgsql import copy_expert_onconflict_skip
from ...config import COMMON_CHUK_SIZE
from ...models import FactDatasetIndex


def load(engine: Engine, dataset_index: pd.DataFrame) -> list:
    pk_name = inspect(FactDatasetIndex).primary_key[0].name
    method = partial(copy_expert_onconflict_skip, return_ids=True, pk=pk_name)
    return dataset_index.to_sql(
        name=FactDatasetIndex.__tablename__,
        con=engine,
        if_exists="append",
        index=False,
        chunksize=COMMON_CHUK_SIZE,
        method=method,
    )
