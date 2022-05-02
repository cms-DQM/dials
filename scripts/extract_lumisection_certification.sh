#!/bin/bash

cd ..

FILE="/eos/user/x/xcoubez/dqm_playground_shared/data/derived/lumisections_flags.pkl"

./manage.py extract_lumisections_certifications $FILE

