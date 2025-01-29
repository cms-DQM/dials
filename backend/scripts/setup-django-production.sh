#!/bin/sh

export "DJANGO_ENV=dummy"
export "DJANGO_SECRET_KEY=dummy"
export "DJANGO_DEBUG=1"
export "DJANGO_ALLOWED_HOSTS=dummy"
export "DJANGO_CSRF_TRUSTED_ORIGINS=dummy"
export "DJANGO_CORS_ALLOWED_ORIGINS=dummy"
export "DJANGO_WORKSPACES={\"dummy\": \"dummy\"}"
export "DJANGO_DATABASE_URI=postgres://dummy:dummy@localhost:5432"
export "DJANGO_DEFAULT_WORKSPACE=dummy"
export "DJANGO_KEYCLOAK_SERVER_URL=dummy"
export "DJANGO_KEYCLOAK_REALM=dummy"
export "DJANGO_KEYCLOAK_CLIENT_ID=dummy"
export "DJANGO_KEYCLOAK_SECRET_KEY=dummy"
export "DJANGO_KEYCLOAK_API_CLIENTS={}"
export "DJANGO_REDIS_URL=dummy"
export "DJANGO_OMS_SSO_CLIENT_ID=dummy"
export "DJANGO_OMS_SSO_CLIENT_SECRET=dummy"
export "DJANGO_KEYTAB_USR=dummy"
export "DJANGO_KEYTAB_PWD=dummy"

python manage.py collectstatic --noinput
