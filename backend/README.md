# MLPlayground

## Components

The backend can be divided in the following components:

* DQMIO File Indexer (raw data indexing)
* DQMIO ETL (raw data ingestion)
* DQMIO Celery Tasks (interface to spec job queue and signals configuration)
* Custom Auth (authentication handling)

### Custom Auth

Component responsible for handling authentication within rest api using two different viewsets: `KeycloakApiTokenViewSet` and `KeycloakExchangeViewSet`. Note: we are using solely the CERN SSO authentication (that is **super** similar no Keycloak underneath).

### DQMIO Celery Tasks

Component responsible for

### DQMIO ETL

Component responsible for executing our ETL (Extract-Transform-Load) pipeline for each indexed file. The pipeline will import all Runs, Lumisections and Histograms to our database.

### DQMIO File Indexer

Component responsible for keeping track of raw data (DQMIO rootfiles) stored in EOS using a database table. It should store good files and bad files metadata (Rootfile's fUUID, file era, number of entries, ...), filepath in EOS filesystem and processing status.

## Local development

Documentation, tips and tricks to develop MLPlayground locally.

### Accessing DQMIO MLPlayground data from EOS

The following commands will mount the specific DQMIO production data from EOS in read-only mode in your home folder:

```bash
mkdir -p $HOME/data_mlplayground_dqmio
sshfs -o default_permissions,ro $USER@lxplus:/eos/project/m/mlplayground/public/DQMIO $HOME/data_mlplayground_dqmio
```

Unmount goes like:

```bash
umount $HOME/data_mlplayground_dqmio
rm -rf $HOME/data_mlplayground_dqmio
```

### Running PostgresSQL

Considering the main application will only communicate with the database using PostgreSQL DBMS (i.e. not messing with database files directly), running the DBMS decoupled from the main application is less stressful and simulates the production environment. It goes without saying that is much easier to run Postgres using Docker. Using the `-v` flag we can bind-mount the data stored inside the container in the host in order to have a persitent database accross development sessions.

```bash
docker run -d \
	--name postgresql_local \
    --restart always \
    -e POSTGRES_USER=postgres \
	-e POSTGRES_PASSWORD=postgres \
	-v /mnt/postgresql_local_docker_data:/var/lib/postgresql/data \
    -p 5432:5432 \
	postgres
```

### Running Redis

```bash
docker run -d \
	--restart always \
	--name redis_local \
	-p 6379:6379 \
	redis
```

### Running Celery Workers

Starting the worker for dqmio_file_indexer queue:

```bash
celery -A mlplayground worker -l INFO -c 1 -n worker1 -Q dqmio_file_indexer_queue
```


Starting the worker for dqmio_etl queue:
```bash
celery -A mlplayground worker -l INFO -c 1 -n worker2 -Q dqmio_etl_queue
```

### Running Celery Beat

Start the beat scheduler:

```bash
celery -A mlplayground beat -l INFO
```
