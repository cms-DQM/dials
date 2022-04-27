#!/bin/bash

cd ..

FILE="/afs/cern.ch/user/x/xcoubez/public/ML4DQM/LS_flags.pkl"

./manage.py extract_lumisections_certifications $FILE

