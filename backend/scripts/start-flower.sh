#!/bin/bash

CURR_PATH=$(pwd)

if [ "$(basename $CURR_PATH)" != "backend" ]; then
    cd "backend" || exit 1
fi

celery -A dials flower
P1=$!

wait $P1
