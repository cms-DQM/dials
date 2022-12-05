#!/bin/bash

source /opt/app-root/src/root/bin/thisroot.sh # Add ROOT to PATH

python manage.py collectstatic --noinput
# python manage.py migrate --run-syncdb # If you want migrations to run at app start


daphne -b 0.0.0.0 -p 8080 --application-close-timeout 60 mlp.asgi:application # Start Django
