#!/bin/bash

source "$(dirname "$0")/utils.sh"

# Check if OC is checked out in the correct project
check_oc_project

# Importing images into OC
oc import-image etl --from=registry.cern.ch/cms-dqmdc/dials-etl --confirm
oc import-image backend --from=registry.cern.ch/cms-dqmdc/dials-backend --confirm
oc import-image frontend --from=registry.cern.ch/cms-dqmdc/dials-frontend --confirm
