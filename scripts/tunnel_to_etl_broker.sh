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

POD_NAME=$(oc get pods | grep redis-etl-broker | awk '{print $1}')
echo "Selected pod: ${POD_NAME}"

oc port-forward $POD_NAME 6380:6379
