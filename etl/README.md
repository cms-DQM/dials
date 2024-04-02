# Data Pipelines

This directory contains the ETL (Extract, Transform, Load) scripts and related files for ingesting DQMIO files.

## Overview

The `etl` directory is responsible for managing the entire data pipeline from DIALS. It is going to discover raw DQMIO data from Data Bookkeeping Service (DBS) indexing all relevant files in each workspace data mart and schedule ETL jobs in its Job Queue backed by Celery. The jobs are simply responsible for copying the files from the worldwide grid, extract and transform the data and load in each workspace data table.

## Workspaces

Workspace? Data Marts? What are that wizardry language? Multiple groups in CMS analyze different kinds of data, when data-taking is taking place general and more specific datasets are generated. Some groups analyze Monitoring Elements (MEs) in a specific dataset to make sure his detector sub-system are working properly. Then, from a data engineering stand point it makes sense to create multiple databases for each group, members of each group will have their own Workspace = Data Marts. Thus benefiting from performance gains and data isolation for having their own data mart.
