#!/bin/bash

cd ..

# testing one file
python manage.py extract_lumisections /eos/project/c/cmsml4dc/ML_2020/UL2018_Data/DF2018A_1D_Complete/ZeroBias_2018A_DataFrame_1D_1.csv

FILES="/eos/project/c/cmsml4dc/ML_2020/UL2018_Data/DF2018A_1D_Complete/*"

# extracting from all files
for f in $FILES

do
  echo "Processing $f file..."
  #python manage.py extract_lumisections $f
done
