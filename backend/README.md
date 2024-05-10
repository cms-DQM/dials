# DIALS

The backend is a simple Django application built on top of Django Rest Framework for connecting to multiple databases depending on users roles and querying data from the database. It is divided in the following components:

* `cern_auth`: Component responsible for handling authentication within rest api using two different authentication classes (`KeycloakAuthentication`, `KeycloakApiTokenAuthentication`) and exposes two viewsets (`KeycloakApiTokenViewSet`, `KeycloakExchangeViewSet`) for api token issue and token exchange. Note: we are using solely the CERN SSO authentication (that is **super** similar no Keycloak underneath);

* `dataset_index`: Retrieve, list and filter data from dataset indexer table;

* `dim_mes`: Retrieve, list and filter data from dimension monitoring elements table;

* `file_index`: Retrieve, list and filter data from file index table;

* `lumisection`: Retrieve, list and filter data from lumisection table;

* `run`: Retrieve, list and filter data from run table;

* `th1`: Retrieve, list and filter data from th1 table;

* `th2`: Retrieve, list and filter data from th2 table;

* `static` & `templates`: Serve swagger html and configuration file.


## Useful sources

* [Integrating Keycloak with Django](https://blog.stackademic.com/integrating-keycloak-with-django-7ae39abe3a0b) (Specifically PART 2)
* [Hot to run periodic tasks in Djando using Celery](https://episyche.com/blog/how-to-run-periodic-tasks-in-django-using-celery)
* [Celery lock question at stackoverflow](https://stackoverflow.com/questions/32321143/allow-a-task-execution-if-its-not-already-scheduled-using-celery)
