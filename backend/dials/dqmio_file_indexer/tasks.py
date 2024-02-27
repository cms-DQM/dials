from utils.redis_lock import run_if_not_locked, with_lock

from dials import celery_app

from .methods import RawDataIndexer


@celery_app.task(queue="dqmio_file_indexer_queue", name="dqmio_file_indexer.tasks.index_files_and_schedule_hists")
@run_if_not_locked(lock_name="LOCK_index_files_and_schedule_hists")
@with_lock(lock_name="LOCK_index_files_and_schedule_hists")
def index_files_and_schedule_hists():
    indexer = RawDataIndexer()
    indexer.start()
    result = indexer.schedule_ingestion()
    return result


@celery_app.task(queue="celery_periodic", name="dqmio_file_indexer.tasks.handle_periodic", ignore_result=True)
@run_if_not_locked(lock_name="LOCK_index_files_and_schedule_hists")
def handle_periodic():
    index_files_and_schedule_hists.apply_async()
