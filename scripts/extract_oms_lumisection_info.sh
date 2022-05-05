#!/bin/bash

cd ..

FILE="/eos/user/x/xcoubez/dqm_playground_shared/data/secondary/ZeroBias_rate_perLS_from_OMS_2018.pkl"

./manage.py extract_oms_lumisection_information_from_file $FILE
