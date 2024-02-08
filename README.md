# DQM ML4AD

The goal of this project is to index, prepare, display and monitor nanoDQMIO data for machine learning development for anomaly detection in CMS sub-systems. Initally developed internally by CMS Tracker team, now migrated to DQM-DC.

## Project structure

* Backend using Django (rest api only)
* Frontend using React.js

## TODO Tracker

* Renew public user token when it expires in frontend and trigger confidential user token exchange for renewed public token
* Add backend and frontend dockerfile, docker-compose and deploy script
* Create documentation
* Create tutorials
* R&D: Use HTCondor for nanoDQMIO file processing
* R&D: Data Lakehouse for easy and fast access to data without risk of database and rest-api throttle when CMS Physicists want to develop/test a model (using SWAN + Spark)
