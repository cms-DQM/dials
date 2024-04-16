#!/bin/bash

REGISTRY_REPO=registry.cern.ch/cms-dqmdc

# Build locally
docker build -f ./etl/Dockerfile.prod -t dials_etl_release .
docker build -f ./backend/Dockerfile -t dials_backend_release .
docker build -f ./frontend/Dockerfile.prod -t dials_frontend_release .

# Tag containers according to remote registry
docker tag dials_etl_release $REGISTRY_REPO/dials-etl
docker tag dials_backend_release $REGISTRY_REPO/dials-backend
docker tag dials_frontend_release $REGISTRY_REPO/dials-frontend

# Login to registry and push containers
docker login https://registry.cern.ch
docker push $REGISTRY_REPO/dials-etl
docker push $REGISTRY_REPO/dials-backend
docker push $REGISTRY_REPO/dials-frontend
