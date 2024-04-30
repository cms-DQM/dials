from ...celery import app
from .pipeline import pipeline


@app.task(name="dataset_indexer_pipeline")
def dataset_indexer_pipeline_task(**kwargs):
    pipeline(**kwargs)
