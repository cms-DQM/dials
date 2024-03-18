#!/bin/bash

CURR_PATH=$(pwd)

if [ "$(basename $CURR_PATH)" != "backend" ]; then
    cd "backend" || exit 1
fi

poetry run celery --app=dials beat --loglevel=INFO --schedule=celerybeat-schedule &
P1=$!
poetry run celery --app=dials worker --loglevel=INFO --concurrency=2 --autoscale=4,2 --hostname=periodic_worker --queues=periodic_scheduler &
P2=$!
poetry run celery --app=dials worker --loglevel=INFO --concurrency=1 --autoscale=1,0 --hostname=indexer_worker --queues=etl_file_indexer &
P3=$!
poetry run celery --app=dials worker --loglevel=INFO --concurrency=1 --autoscale=2,0 --hostname=etl_bulk_worker --queues=etl_bulk_ingestion &
P4=$!
poetry run celery --app=dials worker --loglevel=INFO --concurrency=1 --autoscale=2,0 --hostname=etl_priority_worker --queues=etl_priority_ingestion &
P5=$!
poetry run python manage.py runserver 0.0.0.0:8000
P6=$!

wait $P1 $P2 $P3 $P4 $P5 $P6
