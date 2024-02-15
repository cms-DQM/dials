#!/bin/bash

cd mlplayground

poetry run celery -A mlplayground worker -l INFO -c 1 -n worker1 -Q dqmio_file_indexer_queue &
P1=$!
poetry run celery -A mlplayground worker -l INFO -c 1 -n worker2 -Q dqmio_etl_queue &
P2=$!
poetry run celery -A mlplayground worker -l INFO -n worker3 -Q celery_periodic &
P3=$!
poetry run celery -A mlplayground beat -l INFO &
P4=$!
poetry run python manage.py runserver 0.0.0.0:8000
P5=$!

wait $P1 $P2 $P3 $P4 $P5
