#!/bin/bash

source "$(dirname "$0")/utils.sh"

# Check if OC is checked out in the correct project
check_oc_project

# Select pod
POD_NAME=$(get_pod_name "flower")
echo -e "Selected pod: ${POD_NAME}\n"

# Port forward to it
oc port-forward $POD_NAME 5555:5555
