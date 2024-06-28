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

# Primary dataset download queue
pds_names=()
while IFS= read -r dataset; do
    pds_names+=("$dataset")
done < <(jq -r '.workspaces[].primary_datasets[].name' "$ETL_CONFIG_FPATH" | sort -u)

# Parse databases set in environment
databases_parsed=$(echo $DATABASES | sed 's/[ ][ ]*//g')
IFS=',' read -r -a db_names <<< "$databases_parsed"

# Array of pids to wait
pids_arr=()

# Always use the scheduler
poetry run celery --app=python beat --loglevel=INFO -S redbeat.RedBeatScheduler &
pids_arr+=($!)

# Start the common indexer queue
poetry run celery --app=python worker --loglevel=INFO --concurrency=1 --autoscale=1,0 --max-tasks-per-child=1 --hostname=common-indexer@%h --queues=common-indexer &
pids_arr+=($!)

# Start workers for each workspace
for db_name in "${db_names[@]}"; do
    poetry run celery --app=python worker --loglevel=INFO --concurrency=1 --autoscale=1,0 --max-tasks-per-child=1 --hostname=${db_name}-bulk@%h --queues=${db_name}-bulk &
    pids_arr+=($!)
    poetry run celery --app=python worker --loglevel=INFO --concurrency=1 --autoscale=1,0 --max-tasks-per-child=1 --hostname=${db_name}-priority@%h --queues=${db_name}-priority &
    pids_arr+=($!)
done

# Start downloader workers for each pd
for pd_name in "${pds_names[@]}"; do
    poetry run celery --app=python worker --loglevel=INFO --concurrency=1 --autoscale=1,0 --max-tasks-per-child=1 --hostname=${pd_name}-downloader-bulk@%h --queues=${pd_name}-downloader-bulk &
    pids_arr+=($!)
    poetry run celery --app=python worker --loglevel=INFO --concurrency=1 --autoscale=1,0 --max-tasks-per-child=1 --hostname=${pd_name}-downloader-priority@%h --queues=${pd_name}-downloader-priority &
    pids_arr+=($!)
done

# Start Flower for debugging
poetry run celery --app=python flower
pids_arr+=($!)

# Wait for all pids
wait ${pids_arr[*]}
