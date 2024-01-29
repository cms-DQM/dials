# DQM ML4AD

The goal of this project is to index, prepare, display and monitor nanoDQMIO data for machine learning development for anomaly detection in CMS sub-systems. Initally developed internally by CMS Tracker team, now migrated to DQM-DC.

## Project structure

* Backend using Django (rest api only)
* Frontend using React.js

## TODO Tracker

* Integrate backend and frontend (machine learning view will be mocked for now)
* Add authentication using Django (local development) and CERN SSO for staging and production
* Create dockerfiles and docker-compose
* Deploy scripts and s2i integration
* Create documentation and tutorials
* R&D: Use HTCondor for nanoDQMIO file processing
* R&D: Data Lakehouse for easy and fast access to data without risk of database and rest-api throttle when CMS Physicists want to develop/test a model (using SWAN + Spark)
