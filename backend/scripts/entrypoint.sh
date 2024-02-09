#!/bin/sh

if echo $DJANGO_DATABASE_ENGINE | grep -q *"postgres"*;
then
    echo "Waiting for postgres..."

    while ! nc -z $DJANGO_DATABASE_HOST $DJANGO_DATABASE_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

poetry run mlplayground/manage.py migrate

exec "$@"
