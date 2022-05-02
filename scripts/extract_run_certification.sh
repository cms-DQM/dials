#!/bin/bash

cd ..

FILE="/eos/user/x/xcoubez/dqm_playground_shared/data/derived/runs_flags.pkl"
ORIGINAL_FILE="/eos/user/x/xcoubez/dqm_playground_shared/data/primary/RR-UL-18.csv"

./manage.py extract_run_certifications $FILE

