#!/bin/bash

source "$(dirname "$0")/utils.sh"

# Check if OC is checked out in the correct project
check_oc_project

# Select pod
POD_NAME=$(get_pod_name "redis-etl-broker")
echo -e "Selected pod: ${POD_NAME}\n"

# "SSH" to container in the pod
oc exec -it $POD_NAME -c common-indexer -- bash
