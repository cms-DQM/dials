# Local development

Documentation, tips and tricks to develop DIALS locally. Make sure you are doing all the modifications in your own fork.

## Setup tools

The etl and backend uses `Python` `^3.10.13` , the third-party dependencies are managed by [`poetry`](https://python-poetry.org/) `^1.7.1` and note that explicitly the etl has a hard dependency on `ROOT` `^6.30/02`. After having all these dependencies you can run `poetry install --no-root` to install all the etl and backend dependencies specified in `pyproject.toml`. Then you should configure `pre-commit` by running `poetry run pre-commit install`, this will ensure code standardization.

The frontend uses `Node.js` `^20.11.0` and the third-party dependencies are managed by [`yarn`](https://www.npmjs.com/package/yarn) that can be installed using `npm install -g yarn`. Then you can run `yarn install` to install the frontend dependencies specified in `package.json`. Note that the frontend will not work if code does not agree with `eslint` configuration, to fix any style problems you can run `yarn run lint`.

If you don't want to setup any of those tools you can run the entire stack trough `docker`, you'll only need `pyyaml` package to generate the docker compose file.

## Setup the data used for testing

### Accessing DQMIO data from EOS

Note: This step is *optional*, if you don't mount EOS locally the ETL workflow will download the data locally trough *scp*.

The following command will mount the production data directory from EOS in read-only mode:

```bash
mkdir -p ./DQMIO
sshfs -o default_permissions,ro <YOUR-CERN-USER>@lxplus.cern.ch:/eos/project-m/mlplayground/public/DQMIO_workspaces ./DQMIO
```

In case you need to unmount (turning off the computer/losing connection to lxplus will umount automatically) you can run the following command:

```bash
umount ./DQMIO
```

### Getting data from DBS

The dataset and files indexing pipelines read data from DBS to trigger ETL jobs periodically, so it is important to have a configured grid certificate (check [here](/docs/SETTING_UP_SA.md) how to generate a certificate) that can be used to access DBS. The dataset indexing pipeline is used mainly to gather datasets metadata, so ingesting the entire index is not an issue, but the files indexing pipeline is used to trigger ETL jobs for each DQMIO file which means that if you ingest all the index locally you are going to ingest all DQMIO files.

To avoid running out of space instead of ingesting the entire index you can provide a mocked DBS response to the indexing pipeline, which is enough to test the ingestion locally. An example can be found in `/eos/project-m/mlplayground/public/mocked_dbs_minimal.json`.

### Simulating EOS directory structure

Instead of mounting production DQMIO data, you can setup a directory that behaves exactly like production. This is the only way to run locally if you don't have access to `mlplayground` project area.

You'll need to get some files that can be used for testing depending on how many primary datasets you want to ingest. Let's say you are going to test with `ZeroBias` and `StreamExpress` datasets, run the following commands to simulate the directory structure:

```bash
mkdir -p ./DQMIO
mkdir -p ./DQMIO/ZeroBias
mkdir -p ./DQMIO/StreamExpress
```

Them put all the `ZeroBias` and `StreamExpress` files you want to test the ingestion in each respective directory. Note that you may need to update your `mocked_dbs` file if you are going to use different files than the ones already set in the example.

## Running with Docker

### Setup the environment variables

#### Backend

Create a `.env` file inside [`backend`](/backend/) with the following variables:

```bash
DJANGO_ENV=dev
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
DJANGO_CSRF_TRUSTED_ORIGINS=http://localhost:8000 http://localhost:3000 http://localhost:8081
DJANGO_CORS_ALLOWED_ORIGINS=http://localhost:8000 http://localhost:3000 http://localhost:8081
DJANGO_KEYCLOAK_SERVER_URL=https://auth.cern.ch/auth/
DJANGO_KEYCLOAK_REALM=cern
DJANGO_KEYCLOAK_PUBLIC_CLIENT_ID=cms-dials-dev-public-app
DJANGO_CACHE_TTL=0
DJANGO_SECRET_KEY=potato
DJANGO_REDIS_URL=redis://redis-local:6379/3
DJANGO_DATABASE_URI=postgres://postgres:postgres@postgresql-local:5432
DJANGO_KEYCLOAK_CONFIDENTIAL_CLIENT_ID=cms-dials-dev-confidential-app

DJANGO_WORKSPACES={"csc": "cms-dqm-runregistry-offline-csc-certifiers", "ecal": "cms-dqm-runregistry-offline-ecal-certifiers", "hcal": "cms-dqm-runregistry-offline-hcal-certifiers", "jetmet": "cms-dqm-runregistry-offline-jme-certifiers", "tracker": "cms-dqm-runregistry-offline-tracker-certifiers"}
DJANGO_DEFAULT_WORKSPACE=tracker

DJANGO_KEYCLOAK_CONFIDENTIAL_SECRET_KEY=<SECRET-HERE-1>
DJANGO_KEYCLOAK_API_CLIENTS={"<SECRET-HERE-2>": "cms-dials-dev-api-client-test"}

```

Go to [Application Portal](https://application-portal-qa.web.cern.ch/), get the secrets values and fill where it is written `SECRET_HERE`.

#### ETL

Create a `.env` file inside [`etl`](/etl/) with the following variables:

```bash
ENV=dev
CELERY_BROKER_URL=redis://redis-local:6379/0
CELERY_RESULT_BACKEND=redis://redis-local:6379/1
CELERY_REDBEAT_URL=redis://redis-local:6379/2
DATABASES=csc,ecal,hcal,jetmet,tracker
DATABASE_URI=postgresql://postgres:postgres@postgresql-local:5432
EOS_LANDING_ZONE=/eos/project-m/mlplayground/public/DQMIO_workspaces

CERT_FPATH=<PATH-TO-YOUR>/usercert.pem
KEY_FPATH=<PATH-TO-YOUR>/userkey.open.key
KEYTAB_USER=<YOUR-CERN-USER>
KEYTAB_PWD=<YOUR-CERN-PWD>
MOUNTED_EOS_PATH=<PATH-TO-YOUR>/DQMIO
MOCKED_DBS_FPATH=<PATH-TO-YOUR>/mocked_dbs_minimal.json
ETL_CONFIG_FPATH=<PATH-TO-YOUR>/etl.config.json
```

* `MOUNTED_EOS_PATH` is optional, if you don't mount EOS locally the files will be downloaded trough scp;
* `MOCKED_DBS_FPATH` is optional, if do not set it the application will try to ingest all available files in DBS.

### Starting with docker

The [`etl`](/elt/), [`backend`](/backend/) and [`frontend`](/frontend/) ships a `Dockerfile` that can be used for local development. The repository ships the script [`gencompose-self-contained.py`](/scripts/gencompose-self-contained.py) to automatically generate a docker-compose file based on the environment variables (e.g. related to how many workspace you want to use for development). Beware that you'll need to specify the path you want to persist the postgres data:

```bash
./scripts/gencompose-self-contained.py --pg-persistent-path /mnt/pg-data
```

You can start all services by first building, then starting the database and then starting from the [repository root's directory](/):

```bash
docker compose build
docker compose up dials-init
docker compose up
```

#### Starting the ETL

In order to force the indexing it is possible to run the `trigger-indexing` script from inside the docker container with:

```bash
docker exec -it dials-flower bash -c 'python3 scripts/trigger-indexing.py'
```

#### Monitoring the queues

Tasks can be monitored trough flower, the default username and password for local development is `admin`.

#### Cleaning PG database

```bash
docker compose up dials-purge
```

#### Cleaning Redis database

In case you stop the containers before finishing all tasks in celery queue you may need to clear redis before restarting the ETL from 0, this can be quickly done by flushing the database using `redis-cli` inside the container:

```bash
docker exec -it redis-local bash
redis-cli
flushall
```

#### Notes

- You will notice that the docker compose file is set to bind-mount the code from backend and frontend in the host, so hot reloading works (i.e. you don't need to always build the container upon any modification)!!! In order to this work correctly you need to setup the current user GID and UID when building the container, **generally** UID and GID for single not-hardcore linux user are set to 1000 and both Dockerfiles use that as default values. In case you use a different UID/GID you can set then as build args:

```bash
docker compose build --build-arg UID=$(id -u) --build-arg GID=$(id -g)
```

- In case you need to remove all generated containers you can run:

```bash
docker compose down
docker compose --profile=donotstart down
```

- In case you need to remove all generated images you can run:

```bash
docker images dials\* -q | xargs docker rmi
```


## Running natively

### Running PostgresSQL

Considering the main application will only communicate with the database using PostgreSQL DBMS (i.e. not messing with database files directly), running the DBMS decoupled from the main application is less stressful and successfully simulates the production environment. It goes without saying that is much easier to run Postgres using Docker and using the `-v` flag we can bind-mount the data stored inside the container in the host in order to have a persistent database across development sessions. You can find more information about postgres container [here](https://hub.docker.com/_/postgres).

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

The same arguments used for running PostgreSQL locally also holds for running Redis (our in-memory database acting as message broker for our job queues) locally. Differently from PostgreSQL in development there is not real need for persistent store, so we will launch the counter ephemerally. You can find more information about redis container [here](https://hub.docker.com/_/redis).

```bash
docker run -d \
    --restart always \
    --name redis_local \
    -p 6379:6379 \
    redis
```

### Setup the environment variables

Since we are running postgres and redis trough docker outside the same docker network the application would be execute, we just need to update some environment variables.

#### Backend

Refer to the backend environment variables in docker section and update the following variables:

```bash
DJANGO_REDIS_URL=redis://localhost:6379/3
DJANGO_DATABASE_URI=postgres://postgres:postgres@localhost:5432
```

#### ETL

Refer to the etl environment variables in docker section and update the following variables:

```bash
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1
CELERY_REDBEAT_URL=redis://localhost:6379/2
DATABASE_URI=postgresql://postgres:postgres@localhost:5432
```

### Running the ETL

From within [`repository root's directory`](/) or [`etl`](/etl/) you can use the [`start-dev.sh`](/etl/scripts/start-dev.sh) script or the poe task `poe start-etl` to start the entire etl stack in one command.

Note that before starting the ETL natively you need to setup the database, in order to do this from within [`etl`](/etl/) you can run `alembic upgrade head`. If you need to clean the database you can run `alembic downgrade -1`.

Note: If running the commands separated you should execute then inside the [`etl`](/etl/) directory.

### Running the Backend

From within [`repository root's directory`](/) or [`backend`](/backend/) you can use the [`start-dev.sh`](/backend/scripts/start-dev.sh) script or the poe task `poe start-api` to start the entire backend stack in one command.

Note: If running the commands separated you should execute then inside the [`backend`](/backend/) directory.

### Running the Frontend

Inside the [`frontend`](/frontend/) directory you can using the script `yarn run start` to start the react-scripts development server.

## Choose how many workspace to execute

The ETL part of this application is memory hungry, each celery queue consumes at idle at least 200MiB of RAM. By default we are using one queue for indexing, one queue for the beat scheduler, each workspace needs 2 queues (bulk and priority) and for each unique primary dataset that all workspace depends on we have 2*N downloading queues (bulk and priority).

It is possible to run locally 5 workspaces with 9 unique primary datasets, if you have at least 8GiB of RAM free (keep in mind that the memory consumption can be grater while ingesting the data, because the application will read some DQMIO root files). If you don´t have all this available run you can test the application with few workspaces and primary datasets.

Lets say you want to test only the `tracker` workspace with only the `ZeroBias` dataset, you'll need to modify the following environment variables:

### Backend

```bash
DJANGO_WORKSPACES={"tracker": "cms-dqm-runregistry-offline-tracker-certifiers"}
DJANGO_DEFAULT_WORKSPACE=tracker
```

### ETL

```bash
DATABASES=tracker
```

And you'll also need to update the [`etl.config.json`](/etl/etl.config.json) file:

```json
{
  ...,
  "workspaces": [
    {
      "name": "tracker",
      "primary_datasets": [
        {
          "dbs_pattern": "/ZeroBias/*Run202*/DQMIO",
          "dbs_instance": "global",
          "bulk_downloader_queue": "ZeroBias-downloader-bulk",
          "priority_downloader_queue": "ZeroBias-downloader-priority"
        }
      ],
      "me_startswith": [
        "PixelPhase1/",
        "SiStrip/",
        "Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/TrackEtaPhi_ImpactPoint_GenTk"
      ],
      "bulk_ingesting_queue": "tracker-bulk",
      "priority_ingesting_queue": "tracker-priority"
    }
  ]
  ...
}
```

If you are very limited in RAM you can also decrease the ingestion chunk size in the same file (beware that the ingestion will be slower when you decrease the chunk size):

```json
{
  ...,
  "common_chunk_size": 1000,
  "th2_chunk_size": 200,
  ...
}
```

## CERN's Keycloak QA environment

The QA server is very useful test environment for CERN's authentication service, but you can't reach it if you outside CERN's network. So it is important to always tunnel your connection trough `lxtunnel`, since the QA authentication server can only be accessible trough CERN. For doing that you can use [sshuttle](https://github.com/sshuttle/sshuttle), it is a “poor man’s VPN” solution which works on macOS and Linux. It uses SSH tunnelling to transparently redirect certain parts of your traffic to the internal network.

This is the command I use (I save it in my zshrc file):

```bash
tunnel_to_cern () {
	sshuttle --dns -v -r lxtunnel.cern.ch 137.138.0.0/16 128.141.0.0/16 128.142.0.0/16 188.184.0.0/15 --python=python3
}
```

The `lxtunnel` alias resolves to the following ssh config:

```
Host lxtunnel
        HostName lxtunnel.cern.ch
        User <your-cern-username>
        GSSAPITrustDNS yes
        GSSAPIAuthentication yes
        GSSAPIDelegateCredentials yes
```

More information on tunneling to CERN can be found [here](https://abpcomputing.web.cern.ch/guides/sshtunnel/) and [here](https://codimd.web.cern.ch/vjC8BHbTS7etHwJve-K2Uw#).

Beware that if you running with docker, the docker network will not go trough sshuttle tunnel, so you'll need to run all the containers in the `host` network mode (this do not work on Mac). You can generate a specific docker compose file for this with the script [`gencompose-network-host.py`](/scripts/gencompose-network-host.py). Note that you'll need to start the frontend with `qa` script: `yarn run start:qa`.
