import logging

from celery import states
from celery.signals import before_task_publish, task_prerun, worker_ready
from django.utils import timezone
from django_celery_results.backends.database import DatabaseBackend
from django_celery_results.models import TaskResult
from mlplayground import celery_app
from utils.redis_lock import clear_locks

logger = logging.getLogger(__name__)


@before_task_publish.connect
def create_task_result_on_publish(sender=None, headers=None, **kwargs):
    """
    This is a workaround for an issue where django-celery-results
    is not adding PENDING tasks to the database.

    # ref: https://github.com/celery/django-celery-results/issues/286
    """
    db_result_backend = DatabaseBackend(celery_app)
    registered_task_names = celery_app.tasks.keys()

    if (
        "task" not in headers
        or not db_result_backend
        or sender not in registered_task_names
        or headers["ignore_result"]
    ):
        return

    # essentially transforms a single-level of the headers dictionary
    # into an object with properties
    request = type("request", (object,), headers)

    db_result_backend.store_result(
        headers["id"],
        None,
        states.PENDING,
        traceback=None,
        request=request,
    )


@task_prerun.connect
def update_date_created_prerun(task_id, task, *args, **kwargs):
    """
    This is a workaround to change date_created field in TaskResult
    when task is about to start, so `date_created` always means `date_started`
    """
    if task.request.ignore_result:
        return

    try:
        task_result = TaskResult.objects.get(task_id=task_id)
    except TaskResult.DoesNotExist as err:
        logger.warn(f"Task result {task_id} not found. Err: {str(err)}")
    else:
        task_result.date_created = timezone.now()
        task_result.save()


@worker_ready.connect
def unlock_all(**kwargs):
    """
    When application starts clear possible deadlocks in broker
    """
    clear_locks()
