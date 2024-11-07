from ..env import CELERY_BROKER_URL, CELERY_REDBEAT_URL, CELERY_RESULT_BACKEND


broker_connection_retry_on_startup = True
broker_transport_options = {"visibility_timeout": 21600}  # 6 hours
broker_url = CELERY_BROKER_URL
result_backend = CELERY_RESULT_BACKEND
redbeat_redis_url = CELERY_REDBEAT_URL
task_track_started = True
result_extended = True
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = "UTC"
enable_utc = True
imports = (
    "python.pipelines.dataset_indexer.tasks",
    "python.pipelines.file_indexer.tasks",
    "python.pipelines.file_ingesting.tasks",
    "python.pipelines.ml_inference.tasks",
)
