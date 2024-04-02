from ...celery import app
from ...pipelines.indexer.methods import pipeline as indexer_pipeline


@app.task(name="indexer_pipeline")
def indexer_pipeline_task(**kwargs):
    indexer_pipeline(**kwargs)
