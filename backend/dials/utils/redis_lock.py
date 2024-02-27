from dials import celery_app


def run_if_not_locked(lock_name):
    def decorator(function):
        def wrapper(*args, **kwargs):
            conn = celery_app.broker_connection().default_channel.client
            lock = int(conn.get(lock_name) or 0)
            if lock > 0:
                return
            result = function(*args, **kwargs)
            return result

        return wrapper

    return decorator


def with_lock(lock_name):
    def decorator(function):
        def wrapper(*args, **kwargs):
            conn = celery_app.broker_connection().default_channel.client
            conn.incr(lock_name)
            result = function(*args, **kwargs)
            conn.decr(lock_name)
            return result

        return wrapper

    return decorator


def clear_locks():
    conn = celery_app.broker_connection().default_channel.client
    for key in conn.keys():
        if key.decode("utf-8").startswith("LOCK_"):
            conn.delete(key)
