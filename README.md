# DQM ML4AD

The goal of this project is to index, prepare, display and monitor nanoDQMIO data for machine learning development for anomaly detection in CMS sub-systems. Initally developed internally by CMS Tracker team, now migrated to DQM-DC.

## Project structure

* Backend using Django (rest api only)
* Frontend using React.js

## Planning

* Create documentation (with tutorials for new developers)
    * Backend design
    * Job queues
    * Scheduler
    * Frontend design
    * Backend and frontend communication
    * Authentication flows (user interactively and script/machine non-interactively)
    * Diagrams are super helpful!!!!
    * How to deploy manually (with printscreens)
    * How to contribute (with examples/tutorials)
* R&D: Use HTCondor for nanoDQMIO file processing (discuss if it is worth it)
* R&D: Data Lakehouse for easy and fast access to data without risk of database and rest-api throttle when CMS Physicists want to develop/test a model (using SWAN + Spark)
* R&D: Model registry (model binary + pre-processor script)
* R&D: Continuous inference


## TODO Tracker

* (Backend) Add a name to tasks sent to job queue
* (Backend) Add logic to remove file from BadFileIndex table when it is fixed/removed from filesystem
* (Frontend) Add copyright notice on the home page at the footer
* (Backend) Create viewset for BadFileIndex model
* (Frontend) Add card with bad files count
* (Frontend) Add bad files count bar to `Indexed file by status` bar plot
* (Frontend) Add filter in `Indexed files` tab to look for bad files (different api request)
* (Frontend) Fix eslint warnings
* Openshift deployment with cli + scripts
* Staging deployment
