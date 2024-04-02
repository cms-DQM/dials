from .env import celery_broker_url


broker_connection_retry_on_startup = True
broker_transport_options = {"visibility_timeout": 21600}  # 6 hours
broker_url = celery_broker_url
result_backend = celery_broker_url
task_track_started = True
result_extended = True
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = "UTC"
enable_utc = True
imports = (
    "python.pipelines.indexer.tasks",
    "python.pipelines.ingestor.tasks",
)
