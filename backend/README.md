# MLPlayground

The backend can be divided in the following components:

* `DQMIO File Indexer`: Component responsible for keeping track of raw data (DQMIO rootfiles) stored in EOS using a database table. It should store good files and bad files metadata (Rootfile's fUUID, file era, number of entries, ...), filepath in EOS filesystem and processing status. In the sense of a data architecture it handles the raw data indexing.

* `DQMIO ETL`: Component responsible for executing our ETL (Extract-Transform-Load) pipeline for each indexed file. The pipeline will import all Runs, Lumisections and Histograms to our database. In the sense of a data architecture it handles the raw data ingestion.

* `DQMIO Celery Tasks`: Component responsible for visualizing job queues state, configuring celery signal and generating serializers for api methods that schedule tasks instead returning the actual data.

* `Custom Auth`: Component responsible for handling authentication within rest api using two different authentication classes (`KeycloakAuthentication`, `KeycloakApiTokenAuthentication`) and exposes two viewsets (`KeycloakApiTokenViewSet`, `KeycloakExchangeViewSet`) for api token issue and token exchange. Note: we are using solely the CERN SSO authentication (that is **super** similar no Keycloak underneath).

The data pipeline is depicted in the following image:

![alt text](/docs/img/backend_data_pipeline.png)


## Useful sources

* [Integrating Keycloak with Django](https://blog.stackademic.com/integrating-keycloak-with-django-7ae39abe3a0b) (Specifically PART 2)
* [Hot to run periodic tasks in Djando using Celery](https://episyche.com/blog/how-to-run-periodic-tasks-in-django-using-celery)
* [Celery lock question at stackoverflow](https://stackoverflow.com/questions/32321143/allow-a-task-execution-if-its-not-already-scheduled-using-celery)
