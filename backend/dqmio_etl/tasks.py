import logging

from dials import celery_app

from .methods import HistIngestion


logger = logging.getLogger(__name__)


@celery_app.task
def ingest_function(file_index_id: int):
    ing = HistIngestion(file_index_id)
    result = ing.run()
    return result
