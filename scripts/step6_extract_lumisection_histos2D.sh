#!/bin/bash

cd ..

# testing one file
./manage.py extract_lumisections_histos2D /eos/project/c/cmsml4dc/ML_2020/UL2017_Data/DF2017B_2D_Complete/ZeroBias_2017B_DataFrame_2D_1.csv

FILES="/eos/project/c/cmsml4dc/ML_2020/UL2017_Data/DF2017B_2D_Complete/ZeroBias*"

# extracting from all files
for f in $FILES

do
  echo "Processing $f file..."
  #./manage.py extract_lumisections_histos2D $f
done
