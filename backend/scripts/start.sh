#!/bin/bash

poetry shell
cd mlplayground

celery -A mlplayground worker -l INFO -c 1 -n worker1 -Q dqmio_file_indexer_queue &
P1=$!
celery -A mlplayground worker -l INFO -c 1 -n worker2 -Q dqmio_etl_queue &
P2=$!
celery -A mlplayground beat -l INFO &
P3=$!
./manage.py runserver
P4=$!

wait $P1 $P2 $P3 $P4
