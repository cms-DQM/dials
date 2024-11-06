#!/bin/bash

oc scale --replicas=1 deployment/common-indexer
oc scale --replicas=1 deployment/common-redbeat
oc scale --replicas=1 deployment/flower
oc scale --replicas=1 deployment/csc-bulk
oc scale --replicas=1 deployment/csc-priority
oc scale --replicas=1 deployment/ecal-bulk
oc scale --replicas=1 deployment/ecal-priority
oc scale --replicas=1 deployment/hcal-bulk
oc scale --replicas=1 deployment/hcal-priority
oc scale --replicas=1 deployment/jetmet-bulk
oc scale --replicas=1 deployment/jetmet-priority
oc scale --replicas=1 deployment/tracker-bulk
oc scale --replicas=1 deployment/tracker-priority
oc scale --replicas=1 deployment/private-bulk
oc scale --replicas=1 deployment/egamma-bulk
oc scale --replicas=1 deployment/egamma-priority
