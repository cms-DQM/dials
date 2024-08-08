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
oc scale --replicas=1 deployment/hi-forward0-downloader-bulk
oc scale --replicas=1 deployment/hi-forward0-downloader-priority
oc scale --replicas=1 deployment/hi-physics-raw-prime0-downloader-bulk
oc scale --replicas=1 deployment/hi-physics-raw-prime0-downloader-priority
oc scale --replicas=1 deployment/jetmet-bulk
oc scale --replicas=1 deployment/jetmet-downloader-bulk
oc scale --replicas=1 deployment/jetmet-downloader-priority
oc scale --replicas=1 deployment/jetmet-priority
oc scale --replicas=1 deployment/jetmet0-downloader-bulk
oc scale --replicas=1 deployment/jetmet0-downloader-priority
oc scale --replicas=1 deployment/muon-downloader-bulk
oc scale --replicas=1 deployment/muon-downloader-priority
oc scale --replicas=1 deployment/muon0-downloader-bulk
oc scale --replicas=1 deployment/muon0-downloader-priority
oc scale --replicas=1 deployment/stream-express-downloader-bulk
oc scale --replicas=1 deployment/stream-express-downloader-priority
oc scale --replicas=1 deployment/stream-hi-express-raw-prime-downloader-bulk
oc scale --replicas=1 deployment/stream-hi-express-raw-prime-downloader-priority
oc scale --replicas=1 deployment/tracker-bulk
oc scale --replicas=1 deployment/tracker-priority
oc scale --replicas=1 deployment/zerobias-downloader-bulk
oc scale --replicas=1 deployment/zerobias-downloader-priority
oc scale --replicas=1 deployment/egamma0-downloader-bulk
oc scale --replicas=1 deployment/egamma0-downloader-priority
oc scale --replicas=1 deployment/private-bulk
oc scale --replicas=1 deployment/private-downloader-bulk
oc scale --replicas=1 deployment/egamma-bulk
oc scale --replicas=1 deployment/egamma-priority