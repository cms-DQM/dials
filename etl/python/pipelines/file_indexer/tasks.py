from ...celery import app
from .pipeline import pipeline


@app.task(name="file_indexer_pipeline")
def file_indexer_pipeline_task(**kwargs):
    pipeline(**kwargs)
