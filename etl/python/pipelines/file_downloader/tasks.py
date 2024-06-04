from ...celery import app
from ...common.lxplus_client import XrdcpTimeoutError, XrdcpUnknownError
from .pipeline import pipeline


@app.task(
    name="file_downloader_pipeline",
    autoretry_for=(
        XrdcpTimeoutError,
        XrdcpUnknownError,
    ),
    retry_kwargs={"max_retries": 5},
    retry_backoff=True,
)
def file_downloader_pipeline_task(**kwargs):
    pipeline(**kwargs)
