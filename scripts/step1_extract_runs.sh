#!/bin/bash

cd ..

# testing one file
# ./manage.py extract_runs /eos/project/c/cmsml4dc/ML_2020/PerRun_UL2018_Data/ZeroBias_315257_UL2018.csv

FILES="/eos/project/c/cmsml4dc/ML_2020/PerRun_UL2018_Data/ZeroBia*"

# extracting from all files
for f in $FILES

do
  echo "Processing $f file..."
  ./manage.py extract_runs $f
done
