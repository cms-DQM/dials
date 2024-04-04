#!/bin/bash

CURR_PATH=$(pwd)

if [ "$(basename $CURR_PATH)" != "etl" ]; then
    cd "etl" || exit 1
fi

celery --app=python beat --loglevel=INFO --schedule=celerybeat-schedule &
PID_1=$!

celery --app=python worker --loglevel=INFO --concurrency=1 --autoscale=1,0 --max-tasks-per-child=1 --hostname=csc-indexer@%h --queues=indexer-csc &
PID_1=$!
celery --app=python worker --loglevel=INFO --concurrency=1 --autoscale=1,0 --max-tasks-per-child=1 --hostname=csc-bulk@%h --queues=bulk-csc &
PID_2=$!
celery --app=python worker --loglevel=INFO --concurrency=1 --autoscale=1,0 --max-tasks-per-child=1 --hostname=csc-priority@%h --queues=priority-csc &
PID_3=$!

celery --app=python worker --loglevel=INFO --concurrency=1 --autoscale=1,0 --max-tasks-per-child=1 --hostname=ecal-indexer@%h --queues=indexer-ecal &
PID_4=$!
celery --app=python worker --loglevel=INFO --concurrency=1 --autoscale=1,0 --max-tasks-per-child=1 --hostname=ecal-bulk@%h --queues=bulk-ecal &
PID_5=$!
celery --app=python worker --loglevel=INFO --concurrency=1 --autoscale=1,0 --max-tasks-per-child=1 --hostname=ecal-priority@%h --queues=priority-ecal &
PID_6=$!

celery --app=python worker --loglevel=INFO --concurrency=1 --autoscale=1,0 --max-tasks-per-child=1 --hostname=hcal-indexer@%h --queues=indexer-hcal &
PID_7=$!
celery --app=python worker --loglevel=INFO --concurrency=1 --autoscale=1,0 --max-tasks-per-child=1 --hostname=hcal-bulk@%h --queues=bulk-hcal &
PID_8=$!
celery --app=python worker --loglevel=INFO --concurrency=1 --autoscale=1,0 --max-tasks-per-child=1 --hostname=hcal-priority@%h --queues=priority-hcal &
PID_9=$!

celery --app=python worker --loglevel=INFO --concurrency=1 --autoscale=1,0 --max-tasks-per-child=1 --hostname=tracker-indexer@%h --queues=indexer-tracker &
PID_10=$!
celery --app=python worker --loglevel=INFO --concurrency=1 --autoscale=1,0 --max-tasks-per-child=1 --hostname=tracker-bulk@%h --queues=bulk-tracker &
PID_11=$!
celery --app=python worker --loglevel=INFO --concurrency=1 --autoscale=1,0 --max-tasks-per-child=1 --hostname=tracker-priority@%h --queues=priority-tracker &
PID_12=$!

celery --app=python worker --loglevel=INFO --concurrency=1 --autoscale=1,0 --max-tasks-per-child=1 --hostname=jetmet-indexer@%h --queues=indexer-jetmet &
PID_13=$!
celery --app=python worker --loglevel=INFO --concurrency=1 --autoscale=1,0 --max-tasks-per-child=1 --hostname=jetmet-bulk@%h --queues=bulk-jetmet &
PID_14=$!
celery --app=python worker --loglevel=INFO --concurrency=1 --autoscale=1,0 --max-tasks-per-child=1 --hostname=jetmet-priority@%h --queues=priority-jetmet &
PID_15=$!
celery -A python flower
PID_16=$!

wait $PID_1 $PID_2 $PID_3 $PID_4 $PID_5 $PID_6 $PID_7 $PID_8 $PID_9 $PID_10 $PID_11 $PID_12 $PID_13 $PID_14 $PID_15 $PID_16
