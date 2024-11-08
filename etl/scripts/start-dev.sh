#!/bin/bash

CURR_PATH=$(pwd)

if [ "$(basename $CURR_PATH)" != "etl" ]; then
    cd "etl" || exit 1
fi

# Source .env
if [ -f .env ]; then
    set -a
    source .env
    set +a
else
    echo "File .env not found in $CURR_PATH"
    exit 1
fi

# Ingesting queues
ingesting_queues=()

while IFS= read -r queue_name; do
    ingesting_queues+=("$queue_name")
done < <(jq -r '.workspaces[].bulk_ingesting_queue' "$ETL_CONFIG_FPATH" | sort -u)

while IFS= read -r queue_name; do
    ingesting_queues+=("$queue_name")
done < <(jq -r '.workspaces[].priority_ingesting_queue' "$ETL_CONFIG_FPATH" | sort -u)

ingesting_queues=($(printf "%s\n" "${ingesting_queues[@]}" | sort -u))

# Array of pids to wait
pids_arr=()

# Always use the scheduler
poetry run celery --app=python beat --loglevel=INFO -S redbeat.RedBeatScheduler &
pids_arr+=($!)

# Start the common indexer queue
poetry run celery --app=python worker --loglevel=INFO --concurrency=1 --autoscale=1,0 --max-tasks-per-child=1 --hostname=common-indexer@%h --queues=common-indexer &
pids_arr+=($!)

# Start workers for each workspace
for queue_name in "${ingesting_queues[@]}"; do
    poetry run celery --app=python worker --loglevel=INFO --concurrency=1 --autoscale=1,0 --max-tasks-per-child=1 --hostname=${queue_name}@%h --queues=${queue_name} &
    pids_arr+=($!)
done

# Start Flower for debugging
poetry run celery --app=python flower
pids_arr+=($!)

# Wait for all pids
wait ${pids_arr[*]}
