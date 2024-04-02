from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger

from . import celeryconfig
from .config import workspaces


logger = get_task_logger(__name__)

app = Celery("dials_etl")

app.config_from_object(celeryconfig)

app.conf.beat_schedule = {
    f"{workspace['name']} / Indexer pipeline": {
        "task": "indexer_pipeline",
        "schedule": crontab(minute=0),
        "options": {"queue": workspace["indexer_queue"]},
        "kwargs": {"workspace": workspace},
    }
    for workspace in workspaces
}
