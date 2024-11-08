# Function to check the current project
check_oc_project() {
    CURRENT_PROJECT=$(oc project -q 2>/dev/null)
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
}

# Function to get the pod name containing a specific substring
get_pod_name() {
    local substring=$1
    POD_NAME=$(oc get pods | grep "$substring" | awk '{print $1}')

    if [[ -z "$POD_NAME" ]]; then
        echo "No pod found containing substring '$substring'. Exiting..."
        exit 1
    else
        echo "$POD_NAME"
    fi
}
