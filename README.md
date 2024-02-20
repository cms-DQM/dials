This repository contains all components that make up the CMS DQMDC ML4AD service.

# What is ML4AD?

During a `Run`, the `CMS Experiment` collects particle collision data in `Lumisection` time-frame and the experiment subsystem health is monitored by `shifters` using [DQMGUI](https://github.com/cms-DQM/dqmgui_prod). Multiple shifters for many subsystems monitor the most recent lumisection of the current run plots to check a subsystem's health, but given the number of plots and the limited manpower it is not possible to closely pay attention to all plots during the lumisection time-frame. On the other hand, using certified data it is possible to extract knowledge from old runs (at lumisection-level) to help shifters get a glimpse of detector's health on past runs.

ML4AD is an application designed to simplify the process of extracting knowledge from old data by applying **M**achine **L**earning techniques **for** **A**nomaly **D**etection. It is firstly responsible for indexing, storing pre-processed DQMIO data and serving (i.e. can be used for any exploratory analysis not only machine learning) by a WEB UI and REST Api.

This application was born in CMS Tracker ML as a prototype under the name "MLPlayground" and was migrated to CMS DQMDC as an effort of centralizing anomaly detection techniques for every subsystem.

# Tech stack

This project is a full-stack application written in Python (^3.10) and JavaScript (Node.js ^20.11.0). The backend is built using Django (specifically Django Rest Framework), the job queue is managed by Celery and the frontend is built with plain React. It uses a PostgreSQL database instance for storing all data and Redis in-memory database acting as the message broker for the job queue.

# Documentation

* [Backend](/backend/README.md)
* [Frontend ](/frontend/README.md)
* [Authentication](/docs/AUTHENTICATION.md)
* [Deployment](/docs/DEPLOYMENT.md)

# Planning and TODO

Check development planning [here](/docs/PLANNING.md) and TODO tracker [here](/docs/TODO.md).

# Contributing

Check development guidelines [here](/docs/CONTRIBUTING.md) and local development instructions [here](/docs/LOCAL_DEVELOPMENT.md).
