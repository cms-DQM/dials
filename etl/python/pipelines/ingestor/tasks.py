from ...celery import app
from ...pipelines.ingestor.methods import pipeline as ingestor_pipeline


@app.task(name="ingestor_pipeline")
def ingestor_pipeline_task(**kwargs):
    ingestor_pipeline(**kwargs)
