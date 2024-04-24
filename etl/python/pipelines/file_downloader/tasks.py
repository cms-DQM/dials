from ...celery import app
from .pipeline import pipeline


@app.task(name="file_downloader_pipeline")
def file_downloader_pipeline_task(**kwargs):
    pipeline(**kwargs)
