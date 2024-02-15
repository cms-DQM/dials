from dqmio_etl.tasks import ingest_function
from mlplayground import celery_app
from utils.redis_lock import run_if_not_locked, with_lock

from .methods import RawDataIndexer
from .models import FileIndex, FileIndexStatus
from .serializers import FileIndexResponseSerializer


@celery_app.task(queue="dqmio_file_indexer_queue", name="dqmio_file_indexer.tasks.index_files_and_schedule_hists")
@with_lock(lock_name="LOCK_index_files_and_schedule_hists")
def index_files_and_schedule_hists():
    stats = RawDataIndexer().start()
    stats = FileIndexResponseSerializer(stats, many=True).data
    response = {"n_scanned": 0, "n_indexed_good": 0, "n_indexed_bad": 0, "n_scheduled": 0}
    for dir_result in stats:
        total_added_good = dir_result["added_good"]
        good_ingested_ids = dir_result["good_ingested_ids"]
        response["n_scanned"] += dir_result["total"]
        response["n_indexed_good"] += dir_result["added_good"]
        response["n_indexed_bad"] += dir_result["added_bad"]
        if total_added_good == 0:
            continue

        for ingested_id in good_ingested_ids:
            file_index = FileIndex.objects.get(id=ingested_id)
            file_index.update_status(FileIndexStatus.PENDING)
            del file_index
            ingest_function.delay(ingested_id)
            response["n_scheduled"] += 1

    return response


@celery_app.task(queue="celery_periodic", name="dqmio_file_indexer.tasks.handle_periodic", ignore_result=True)
@run_if_not_locked(lock_name="LOCK_index_files_and_schedule_hists")
def handle_periodic():
    index_files_and_schedule_hists.apply_async()
