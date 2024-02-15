from celery import states
from celery.signals import before_task_publish, worker_ready
from django_celery_results.backends.database import DatabaseBackend
from mlplayground import celery_app
from utils.redis_lock import clear_locks


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


# Release all locks
@worker_ready.connect
def unlock_all(**kwargs):
    clear_locks()
