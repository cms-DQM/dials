#!/bin/bash

cd ..

FILE="/afs/cern.ch/user/x/xcoubez/public/ML4DQM/RR_unfolded.pkl"
ORIGINAL_FILE="/afs/cern.ch/user/x/xcoubez/public/ML4DQM/RR-UL-18.csv"

./manage.py extract_run_certifications $FILE

