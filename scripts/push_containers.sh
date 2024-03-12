#!/bin/bash

# Build locally
docker build -f ./backend/Dockerfile -t dials-backend-base .
docker build -f ./frontend/Dockerfile.prod -t dials-frontend .

# Tag containers according to remote registry
docker tag dials-backend-base registry.cern.ch/cms-dqmdc/dials-backend-base
docker tag dials-frontend registry.cern.ch/cms-dqmdc/dials-frontend

# Login to registry and push containers
docker login https://registry.cern.ch
docker push registry.cern.ch/cms-dqmdc/dials-backend-base
docker push registry.cern.ch/cms-dqmdc/dials-frontend
