from celery.signals import worker_ready
from utils.redis_lock import clear_locks


# Release all locks
@worker_ready.connect
def unlock_all(**kwargs):
    clear_locks()
