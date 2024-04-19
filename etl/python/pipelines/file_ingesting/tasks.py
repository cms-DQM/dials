from ...celery import app
from .pipeline import pipeline


@app.task(name="file_ingesting_pipeline")
def file_ingesting_pipeline_task(**kwargs):
    pipeline(**kwargs)
