#!/bin/bash

oc scale --replicas=0 deployment/common-indexer
oc scale --replicas=0 deployment/common-redbeat
oc scale --replicas=0 deployment/flower
oc scale --replicas=0 deployment/csc-bulk
oc scale --replicas=0 deployment/csc-priority
oc scale --replicas=0 deployment/ecal-bulk
oc scale --replicas=0 deployment/ecal-priority
oc scale --replicas=0 deployment/hcal-bulk
oc scale --replicas=0 deployment/hcal-priority
oc scale --replicas=0 deployment/jetmet-bulk
oc scale --replicas=0 deployment/jetmet-priority
oc scale --replicas=0 deployment/tracker-bulk
oc scale --replicas=0 deployment/tracker-priority
oc scale --replicas=0 deployment/private-bulk
oc scale --replicas=0 deployment/egamma-bulk
oc scale --replicas=0 deployment/egamma-priority
