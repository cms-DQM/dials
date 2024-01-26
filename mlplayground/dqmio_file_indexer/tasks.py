from mlplayground import celery_app

from .methods import RawDataIndexer
from .serializers import FileIndexResponseSerializer


@celery_app.task(queue="dqmio_file_indexer_queue")
def index_raw_data():
    stats = RawDataIndexer.start()
    stats = FileIndexResponseSerializer(stats, many=True)
    return stats.data
