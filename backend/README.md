# MLPlayground

The backend can be divided in the following components:

* `DQMIO File Indexer`: Component responsible for keeping track of raw data (DQMIO rootfiles) stored in EOS using a database table. It should store good files and bad files metadata (Rootfile's fUUID, file era, number of entries, ...), filepath in EOS filesystem and processing status. In the sense of a data architecture it handles the raw data indexing.

* `DQMIO ETL`: Component responsible for executing our ETL (Extract-Transform-Load) pipeline for each indexed file. The pipeline will import all Runs, Lumisections and Histograms to our database. In the sense of a data architecture it handles the raw data ingestion.

* `DQMIO Celery Tasks`: Component responsible for visualizing job queues state, configuring celery signal and generating serializers for api methods that schedule tasks instead returning the actual data.

* `Custom Auth`: Component responsible for handling authentication within rest api using two different viewsets: `KeycloakApiTokenViewSet` and `KeycloakExchangeViewSet`. Note: we are using solely the CERN SSO authentication (that is **super** similar no Keycloak underneath).

The data pipeline is depicted in the following image:

![alt text](/docs/img/backend_data_pipeline.png)
