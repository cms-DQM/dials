#!/bin/bash

# Check if a project is currently set
CURRENT_PROJECT=$(oc project -q 2>/dev/null)

# Verify the project is set and contains dials
CHECK_SUB="cms-dials"
if [[ -z "$CURRENT_PROJECT" ]]; then
    echo "No project is currently selected. Exiting..."
    exit 1
elif [[ "$CURRENT_PROJECT" != *${CHECK_SUB}* ]]; then
    echo "The current project does not contain the required substring '${CHECK_SUB}'. Exiting..."
    exit 1
else
    echo "Current project: $CURRENT_PROJECT"
fi

oc import-image etl --from=registry.cern.ch/cms-dqmdc/dials-etl --confirm
oc import-image backend --from=registry.cern.ch/cms-dqmdc/dials-backend --confirm
oc import-image frontend --from=registry.cern.ch/cms-dqmdc/dials-frontend --confirm
