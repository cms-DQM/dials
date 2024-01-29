from mlplayground import celery_app
from dqmio_etl.tasks import ingest_function

from .models import FileIndex, FileIndexStatus
from .methods import RawDataIndexer
from .serializers import FileIndexResponseSerializer


@celery_app.task(queue="dqmio_file_indexer_queue")
def index_raw_data():
    stats = RawDataIndexer().start()
    stats = FileIndexResponseSerializer(stats, many=True)
    return stats.data


@celery_app.task(queue="dqmio_file_indexer_queue", ignore_result=True)
def handle_multi_ingestion(indexer_results):
    for dir_result in indexer_results:
        total_added = dir_result["added"]
        ingested_ids = dir_result["ingested_ids"]
        if total_added == 0:
            continue

        for ingested_id in ingested_ids:
            file_index = FileIndex.objects.get(id=ingested_id)
            file_index.update_status(FileIndexStatus.PENDING)
            del file_index
            ingest_function.delay(ingested_id)


@celery_app.task(queue="dqmio_file_indexer_queue", ignore_result=True)
def chain_index_and_ingestion():
    index_raw_data.apply_async(link=handle_multi_ingestion.s())
