#!/bin/sh

# When testing locally with gunicorn (instead of django runserver) we don't need to copy static files
# Setting the env variable DJANG_DEBUG=1 will handle the static file serving
if [ "$DJANGO_ENV" != "dev" ]; then
    mkdir -p /var/www/api/
    cp -R staticfiles /var/www/api/static
fi

python -m gunicorn dials.asgi:application -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
