#!/bin/sh

# When testing locally with gunicorn (instead of django runserver) we don't need to copy static files
# Setting the env variable DJANG_DEBUG=1 will handle the static file serving
if [ "$DJANGO_ENV" != "dev" ]; then
    mkdir -p /var/www/api/
    cp -R staticfiles /var/www/api/static
fi

if [ "${GUNICORN_LOG_TO_STDOUT}" == 1 ]; then
    extra_args="--access-logfile=- --error-logfile=-"
fi

python -m gunicorn dials.wsgi:application --bind 0.0.0.0:8000 --workers ${GUNICORN_N_WORKERS:=3} --timeout ${GUNICORN_TIMEOUT:=30} $extra_args
