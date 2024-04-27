# Local development

Documentation, tips and tricks to develop DIALS locally.

## Setup environment

The backend uses `Python` `^3.10.13`, the third-party dependencies are managed by [`poetry`](https://python-poetry.org/) `^1.7.1` and has a hard dependency on `ROOT` `^6.30/02`. After having all these dependencies you can run `poetry install --no-root` to install all the backend dependencies specified in `pyproject.toml`. Then you should configure `pre-commit` by running `poetry run pre-commit install`, this will ensure code standardization.

The frontend uses `Node.js` `^20.11.0` and the third-party dependencies are managed by [`yarn`](https://www.npmjs.com/package/yarn) that can be installed using `npm install -g yarn`. Then you can run `yarn install` to install the frontend dependencies specified in `package.json`. Note that the frontend will not work if code does not agree with `eslint` configuration, to fix any style problems you can run `yarn run lint`.

## Tunneling to CERN

When development outside CERN network is important to always tunnel your connection trough `lxtunnel`, since the QA authentication server can only be accessible trough CERN. For doing that you can use [sshuttle](https://github.com/sshuttle/sshuttle), it is a “poor man’s VPN” solution which works on macOS and Linux. It uses SSH tunnelling to transparently redirect certain parts of your traffic to the internal network.

This is the command I use (I save it in my zshrc file):

```bash
tunnel_to_cern () {
	sshuttle --dns -vr lxtunnel 137.138.0.0/16 128.141.0.0/16 128.142.0.0/16 188.184.0.0/15 --python=python3
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

More information on tunneling to CERN can be foudn [here](https://abpcomputing.web.cern.ch/guides/sshtunnel/) and [here](https://codimd.web.cern.ch/vjC8BHbTS7etHwJve-K2Uw#).

## Accessing DQMIO data from EOS

Note: This step is *optional*, if you don't mount EOS locally the ETL workflow will download the data locally trough *scp*.

The following commands will mount the specific DQMIO production data from EOS in read-only mode mimicking lxplus/openshift eos mounting structure:

```bash
sudo mkdir -p /eos/project-m/mlplayground/public/DQMIO_workspaces
sudo mkdir -p /eos/home-m/mlplayground/DQMIO_workspaces
sudo chown -R $USER:$USER /eos
sshfs -o default_permissions,ro mlplayground@lxplus:/eos/project-m/mlplayground/public/DQMIO_workspaces /eos/project-m/mlplayground/public/DQMIO_workspaces
sshfs -o default_permissions,ro mlplayground@lxplus:/eos/home-m/mlplayground/DQMIO_workspaces /eos/home-m/mlplayground/DQMIO_workspaces
```

In case you need to unmount (turning off the computer/losing connection to lxplus will umount automatically) you can run the following command:

```bash
umount /eos/project-m/mlplayground/public/DQMIO_workspaces
umount /eos/home-m/mlplayground/DQMIO_workspaces
```

## Getting data from DBS

The dataset and files indexing pipelines read data from DBS to trigger ETL jobs periodically, so it is important to have a configured grid certificate (check [here](/docs/SETTING-UP-SA.md) how to generate a certificate) that can be used to access DBS. The dataset indexing pipeline is used mainly to gather datasets metadata, so ingesting the entire index is not an issue, but the files indexing pipeline is used to trigger ETL jobs for each DQMIO file which means that if you ingest all the index locally you are going to ingest all DQMIO files.

To avoid running out of space instead of ingesting the entire index you can provide a mocked DBS response to the indexing pipeline, which is enough to test the ingestion locally. An example can be found in `/eos/project-m/mlplayground/public/mocked_dbs_files.json`.

## Running PostgresSQL

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

## Running Redis

The same arguments used for running PostgreSQL locally also holds for running Redis (our in-memory database acting as message broker for our job queues) locally. Differently from PostgreSQL in development there is not real need for persistent store, so we will launch the counter ephemerally. You can find more information about redis container [here](https://hub.docker.com/_/redis).

```bash
docker run -d \
    --restart always \
    --name redis_local \
    -p 6379:6379 \
    redis
```

# Environment variables

For development you can set how many workspaces your hardware can handle (more workspace = more cpu and ram usage during ETL). Limit the number of workspace in the following variables: `DJANGO_WORKSPACES` and `DATABASES`.

## Backend

Create a `.env` file inside [`backend`](/backend/) with the following variables:

```bash
DJANGO_ENV=dev
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
DJANGO_CSRF_TRUSTED_ORIGINS=http://localhost:8000 http://localhost:3000 http://localhost:8081
DJANGO_CORS_ALLOWED_ORIGINS=http://localhost:8000 http://localhost:3000 http://localhost:8081
DJANGO_WORKSPACES={"csc": "cms-dqm-runregistry-offline-csc-certifiers", "ecal": "cms-dqm-runregistry-offline-ecal-certifiers", "hcal": "cms-dqm-runregistry-offline-hcal-certifiers", "jetmet": "cms-dqm-runregistry-offline-jme-certifiers", "tracker": "cms-dqm-runregistry-offline-tracker-certifiers"}
DJANGO_DEFAULT_WORKSPACE=tracker
DJANGO_KEYCLOAK_SERVER_URL=https://keycloak-qa.cern.ch/auth/
DJANGO_KEYCLOAK_REALM=cern
DJANGO_KEYCLOAK_PUBLIC_CLIENT_ID=cms-dials-public-app
DJANGO_SECRET_KEY=potato
DJANGO_REDIS_URL=redis://localhost:6379/3
DJANGO_DATABASE_URI=postgres://postgres:postgres@localhost:5432
DJANGO_KEYCLOAK_CONFIDENTIAL_CLIENT_ID=cms-dials-confidential-app
DJANGO_KEYCLOAK_CONFIDENTIAL_SECRET_KEY=SECRET_HERE_1
DJANGO_KEYCLOAK_API_CLIENTS={"SECRET_HERE_2": "cms-dials-api-client-1"}
```

Login to [QA Application Portal](https://application-portal-qa.web.cern.ch/), get the secrets values and fill where it is written `SECRET_HERE`.

## ETL

Create a `.env` file inside [`etl`](/etl/) with the following variables:

```bash
ENV=dev
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1
CELERY_REDBEAT_URL=redis://localhost:6379/2
DATABASES=csc,ecal,hcal,jetmet,tracker
DATABASE_URI=postgresql://postgres:postgres@localhost:5432
CERT_FPATH=/path/to/usercert.pem
KEY_FPATH=/path/to/userkey.pem
KEYTAB_USER=<lxplus-account>
KEYTAB_PWD=<lxplus-password>
EOS_LANDING_ZONE=/eos/project-m/mlplayground/public/DQMIO_workspaces
MOUNTED_EOS_PATH=/eos/project-m/mlplayground/public/DQMIO_workspaces
MOCKED_DBS_FPATH=/path/to/mocked/dbs/file
```

* `MOUNTED_EOS_PATH` is optional, if you don't mount EOS locally the files will be downloaded trough scp;
* `MOCKED_DBS_FPATH` is optional, if not set it will try to ingest all available files indexed in DBS.

# Running the project components

## [Natively] ETL

From within [`repository root's directory`](/) or [`etl`](/etl/) you can use the [`start-dev.sh`](/etl/scripts/start-dev.sh) script or the poe task `poe start-etl` to start the entire etl stack in one command.

Note that before starting the ETL natively you need to setup the database, in order to do this from within [`etl`](/etl/) you can run `alembic upgrade head`. If you need to clean the database you can run `alembic downgrade -1`.

Note: If running the commands separated you should execute then inside the [`etl`](/etl/) directory.

## [Natively] Backend

From within [`repository root's directory`](/) or [`backend`](/backend/) you can use the [`start-dev.sh`](/backend/scripts/start-dev.sh) script or the poe task `poe start-api` to start the entire backend stack in one command.

Note: If running the commands separated you should execute then inside the [`backend`](/backend/) directory.

## [Natively] Frontend

Inside the [`frontend`](/frontend/) directory you can using the script `yarn run start` to start the react-scripts development server.

## Docker

The [`etl`](/elt/), [`backend`](/backend/) and [`frontend`](/frontend/) ships a `Dockerfile` that can be used for local development. The repository ships the script [`generate-compose.py`](/scripts/generate-compose.py) to automatically generate a docker-compose file based on the environment variables (e.g. related to how many workspace you want to use for development). You can start all services by first building, then starting the database and then starting from the [repository root's directory](/):

```bash
docker compose build
docker compose up dials-init
docker compose up
```

In case you need to clean the database you can run:

```bash
docker compose up dials-purge
```

You will notice that the docker compose file is set to bind-mount the code from backend and frontend in the host, so hot reloading works (i.e. you don't need to always build the container upon any modification)!!! In order to this work correctly you need to setup the current user GID and UID when building the container, **generally** UID and GID for single not-hardcore linux user are set to 1000 and both Dockerfiles use that as default values. In case you use a different UID/GID you can set then as build args:

```bash
docker compose build --build-arg UID=$(id -u) --build-arg GID=$(id -g)
```

Note that we are not using the `-d` flag for running detached from the current terminal, that is a good idea for development sessions and since we are not specifying any docker compose file it is automatically choosing the base file.
