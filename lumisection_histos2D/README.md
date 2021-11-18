# Lumisection Histos 2D

This application is meant to store information about 2D histograms at per lumisection level.

## 1. Base class

...

## 2. Filling the database

A script is provided which runs over the ML4DQM files and extract information regarding the 2D histograms. While doing so, it creates the unique run / lumisection if it doesn't already exist.

From the main repository:
```bash
./manage.py extract_lumisections_histos2D /eos/project/c/cmsml4dc/ML_2020/UL2017_Data/DF2017B_2D_Complete/ZeroBias_2017B_DataFrame_2D_1.csv
```
