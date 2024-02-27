#!/bin/bash

if test -f ".env"; then
  export $(grep "DJANGO_DATABASE_ENGINE" .env)
  export $(grep "DJANGO_DATABASE_HOST" .env)
  export $(grep "DJANGO_DATABASE_PORT" .env)
  export $(grep "DJANGO_CELERY_BROKER_URL" .env)
fi

# Checking if Postgres is alive
if echo $DJANGO_DATABASE_ENGINE | grep "postgres";
then
    echo "Waiting for postgres..."

    while ! nc -z $DJANGO_DATABASE_HOST $DJANGO_DATABASE_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL is alive"
fi

# Checking if Redis is alive
if echo $DJANGO_CELERY_BROKER_URL | grep "redis";
then
  echo "Waiting for redis..."

  redis_host=$(echo $DJANGO_CELERY_BROKER_URL | sed -n 's/.*\/\/\([^:]*\):.*/\1/p')
  redis_port=$(echo $DJANGO_CELERY_BROKER_URL | awk -F: '{print $NF}')

  while ! nc -z $redis_host $redis_port; do
    sleep 0.1
  done

  echo "Redis is alive"
fi

# Migrate if development
if [ "$DJANGO_ENV" = "development" ];
then
  python3 dials/manage.py migrate
fi

exec "$@"
