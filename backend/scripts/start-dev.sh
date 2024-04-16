#!/bin/bash

CURR_PATH=$(pwd)

if [ "$(basename $CURR_PATH)" != "backend" ]; then
    cd "backend" || exit 1
fi

poetry run python manage.py runserver 0.0.0.0:8000
