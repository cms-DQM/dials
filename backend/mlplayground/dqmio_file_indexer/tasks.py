from dqmio_etl.tasks import ingest_function
from mlplayground import celery_app

from .methods import RawDataIndexer
from .models import FileIndex, FileIndexStatus
from .serializers import FileIndexResponseSerializer


@celery_app.task(queue="dqmio_file_indexer_queue")
def index_raw_data():
    stats = RawDataIndexer().start()
    stats = FileIndexResponseSerializer(stats, many=True)
    return stats.data


@celery_app.task(queue="dqmio_file_indexer_queue", ignore_result=True)
def handle_multi_ingestion(indexer_results):
    for dir_result in indexer_results:
        total_added_good = dir_result["added_good"]
        good_ingested_ids = dir_result["good_ingested_ids"]
        if total_added_good == 0:
            continue

        for ingested_id in good_ingested_ids:
            file_index = FileIndex.objects.get(id=ingested_id)
            file_index.update_status(FileIndexStatus.PENDING)
            del file_index
            ingest_function.delay(ingested_id)


@celery_app.task(queue="dqmio_file_indexer_queue", ignore_result=True)
def chain_index_and_ingestion():
    index_raw_data.apply_async(link=handle_multi_ingestion.s())
