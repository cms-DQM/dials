#!/bin/bash

python manage.py collectstatic --noinput

daphne -b 0.0.0.0 -p 8080 mysite.asgi:application
