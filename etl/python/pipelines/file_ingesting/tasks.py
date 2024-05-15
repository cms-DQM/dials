from ...celery import app
from .exceptions import PipelineCopyError, PipelineRootfileError
from .pipeline import pipeline


@app.task(
    name="file_ingesting_pipeline",
    autoretry_for=(
        PipelineCopyError,
        PipelineRootfileError,
    ),
    retry_kwargs={"max_retries": 5},
    retry_backoff=True,
)
def file_ingesting_pipeline_task(**kwargs):
    pipeline(**kwargs)
