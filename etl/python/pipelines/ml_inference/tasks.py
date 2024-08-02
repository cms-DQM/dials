from ...celery import app
from .pipeline import pipeline


@app.task(
    name="ml_inference_pipeline",
)
def ml_inference_pipeline_task(**kwargs):
    pipeline(**kwargs)
