# Local development

Instruction for getting a local version of DIALS for development purposes. By following these intructions, you will have a fully functional version of DIALS (including the data finding, data downloading and ingesting, frontend rendering, and API) that runs locally on your computer, useful for debugging an issue or developing new features.

Note: make sure you are doing all the modifications to this repository (if any) in your own fork, and then make a pull request to merge them in the production repository; do not make changes directly in the production repository.

## Get a local version of the DIALS repository
First, make your own fork of the DIALS repository on GitHub. Then, make a local instance on your computer using the usual `git clone`, for exampe:

```
git clone https://github.com/<YOUR GITHUB USERNAME>/dials.git
```

## Get some data used for testing
The first step is to get some DQMIO data that will be used by your local instance of DIALS. There are essentially two methods: the first one is mounting the real DIALS production workspace (where the files are already gathered by the production DIALS instance) so it can be read by your local instance as well; the second one is copying a small number of DQMIO files to your local machine. Whatever method you choose, you will anyway need a grid certificate for querying DBS (the central CMS file database, basically the backend behind [DAS](https://cmsweb.cern.ch/das/)). Even in case where you will use locally copied files, you still need the grid certificate because the dataset metadata will be queried anyway. Check [here](/docs/SETTING_UP_SA.md) how to generate a certificate. You can put the resulting `usercert.pem` and `userkey.pem` in a location of your choice, and provide the path as an environment variable (see instructions further below).

DIALS will execute an indexing pipeline, querying all available datasets and all available files within each dataset from DBS. The dataset index just contains the names and some metadata on the available datasets, so querying it is not a problem. However, the file index is used to trigger file download and/or ingestion jobs, implying that your local DIALS instance will attempt to download and/or ingest a huge number of DQMIO files. To avoid running out of space, you can provide a dummy DBS response to the indexing pipeline. This dummy response just contains a few files, that should be enough for testing and debugging. An example can be found in `etl/mocks/dbs.json`. To activate it, you have to provide the path to this file as an environment variable (see instruction further below).

### Accessing DQMIO data from EOS by mounting it locally
The first way of accessing the data is by mounting the appropriate EOS directory locally. Note that if you don't mount EOS locally, the file downloading and ingestion workflow will attempt to download the data locally trough *scp*. In that case, you would probably want to use the dummy DBS response instead of the actual DBS response (as mentioned above) to avoid downloading and ingesting a huge number of files.

The following command will mount the production data directory from EOS in read-only mode:

```bash
mkdir -p ./DQMIO_samples
sshfs -o default_permissions,ro <YOUR-CERN-USER>@lxplus.cern.ch:/eos/project-m/mlplayground/public/DQMIO_workspaces ./DQMIO_samples
```

In case you need to unmount (turning off the computer/losing connection to lxplus will umount automatically) you can run the following command:

```bash
umount ./DQMIO_samples
```

(Note the use of `umount` rather than `unmount`.)

Note: this approach can give issues if you use Docker for running DIALS (see below), since the mount does not seem to be visible inside the Docker container.
Therefore, the second approach, discussed below, is recommended.

### Accessing DQMIO data by making a local copy
Instead of mounting the production DQMIO data, you can setup a directory that behaves exactly like production.
To use this approach, simply copy the content of the folder `/eos/project-m/mlplayground/public/DQMIO_samples` into a new `DQMIO_samples` folder in the top directory of the DIALS repository, e.g. as follows:

```
mkdir -p ./DQMIO_samples
scp -r <YOUR LXPLUS USERNAME>@lxplus.cern.ch:/eos/project-m/mlplayground/public/DQMIO_samples/* DQMIO_samples
```

Note: you should make sure that your dummy DBS response file is in sync with the files you actually copy to the local directory. They are in sync at the time of writing, but you might need to make modifications if you are using different files than the ones already set in the example.

## Building and running a local DIALS instance using a Docker container
There are two broad approaches for setting up the environment and running a local version of DIALS: the first involves setting up the environment yourself, which can be a bit of a mess, but is easier once it is set up correctly; the second one uses a docker container instead, which is easier to set up but a little more tricky to interact with while developing. The latter approach is detailed here, the former in the next section.

### Installing Docker
The advantage of using Docker is that you don't need a lot of packages or other dependencies.
You will however need the packages `pyyaml` and `python-decouple`. You can install them using `pip install pyyaml python-decouple`.

For installing Docker, follow the steps here: https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository.
Use the instructions under ‘Install using the apt repository’.
If you already have docker installed, you can skip this step, or follow the instructions for upgrading instead of installing.

Then, follow some additional steps here to avoid typing sudo every time: https://docs.docker.com/engine/install/linux-postinstall/.
It seems necessary to reboot the computer for these changes to take effect.

### Setup the backend environment variables

Create a `.env` file inside the [`backend`](/backend/) folder with the following variables:

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

DJANGO_WORKSPACES={"csc": "cms-dqm-runregistry-offline-csc-certifiers", "ecal": "cms-dqm-runregistry-offline-ecal-certifiers", "egamma": "cms-dqm-runregistry-offline-ecal-certifiers", "hcal": "cms-dqm-runregistry-offline-hcal-certifiers", "jetmet": "cms-dqm-runregistry-offline-jme-certifiers", "muon_staging": "unknown", "tracker": "cms-dqm-runregistry-offline-tracker-certifiers"}
DJANGO_DEFAULT_WORKSPACE=tracker

DJANGO_KEYCLOAK_CONFIDENTIAL_SECRET_KEY=<SECRET-HERE-1>
DJANGO_KEYCLOAK_API_CLIENTS={"<SECRET-HERE-2>": "cms-dials-dev-api-client-test"}

```

- Note: you need to fill in the application secret in the last two lines. Go to the [Application Portal](https://application-portal-qa.web.cern.ch/), get the secrets values and fill where it is written `SECRET_HERE`.

- Note: optionally, you can also modify the `DJANGO_WORKSPACES`, for example if you're only interested in a single workspace for your purposes.

### Setup the ETL environment variables

Create a `.env` file inside the [`etl`](/etl/) folder with the following variables:

```bash
ENV=dev
CELERY_BROKER_URL=redis://redis-local:6379/0
CELERY_RESULT_BACKEND=redis://redis-local:6379/1
CELERY_REDBEAT_URL=redis://redis-local:6379/2
DATABASES=csc,ecal,hcal,jetmet,tracker
DATABASES=csc,ecal,egamma,hcal,jetmet,muon_staging,tracker
DATABASE_URI=postgresql://postgres:postgres@postgresql-local:5432
EOS_LANDING_ZONE=/eos/project-m/mlplayground/public/DQMIO_workspaces

CERT_FPATH=<PATH-TO-YOUR>/usercert.pem
KEY_FPATH=<PATH-TO-YOUR>/userkey.pem
KEYTAB_USER=<YOUR-CERN-USER>
KEYTAB_PWD=<YOUR-CERN-PWD>
MOUNTED_EOS_PATH=<PATH-TO-YOUR>/DQMIO_samples
MOCKED_DBS_FPATH=<PATH-TO-YOUR>/mocks/dbs.json
ETL_CONFIG_FPATH=<PATH-TO-YOUR>/etl.config.json
```

- Note: `MOUNTED_EOS_PATH` is optional, if you don't mount EOS locally the files will be downloaded trough scp;
- Note: `MOCKED_DBS_FPATH` is optional, if do not set it the application will try to ingest all available files in DBS.

### Building and launching the Docker container

The [`etl`](/elt/), [`backend`](/backend/) and [`frontend`](/frontend/) ship a `Dockerfile` that can be used for local development. Furthermore, the DIALS repository ships the script [`gencompose-self-contained.py`](/scripts/gencompose-self-contained.py) to automatically generate a docker-compose file based on the environment variables (e.g. related to how many workspace you want to use for development). You can optionally specify a path to where your local DIALS instance will store its database. This is useful to not have to re-download and/or re-ingest the files every time you launch your DIALS instance; instead it will read the database from where you stored it in a previous session.

```bash
./scripts/gencompose-self-contained.py --pg-persistent-path /mnt/dials-pg-data
```

You can start all services by first building, then starting the database and then starting from the [repository root's directory](/):

```bash
docker compose build
docker compose up dials-init
docker compose up
```

Note: in some cases, `Permission denied errors` might show up related to the `userkey.pem` file when starting the indexing pipeline (see instructions below), even though the `userkey.pem` file is correctly set and publicly readable. If this occurs, you might want to check your user ID and group ID with `echo $(id -u)` and `echo $(id -g)` respectively. If they are not equal to the standard (`1000`), you should replace the `docker compose build` above by the modified command below:

```
docker compose build --build-arg UID=$(id -u) --build-arg GID=$(id -g)
```

After running `docker compose up`, you should see a whole bunch of messages in the terminal. Once you start seeing messages ending in `Events of group {task} enabled by remote.`, the launch is complete and DIALS is up and running!
You can additionally check that DIALS is correctly running by running the command (in a separate terminal) `docker ps`. If everything went well, you should see something like this:

```
CONTAINER ID   IMAGE            COMMAND                  CREATED         STATUS                   PORTS                                       NAMES
9549095739c5   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 3 minutes                                                         dials-jetmet-downloader-priority
81765d44592e   dials_frontend   "docker-entrypoint.s…"   3 minutes ago   Up 3 minutes             0.0.0.0:3000->3000/tcp, :::3000->3000/tcp   dials-frontend
fe3bfd7c084c   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 3 minutes                                                         dials-csc-bulk
88a01dc0e518   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 3 minutes                                                         dials-hiphysicsrawprime0-downloader-priority
fec0501e6d1c   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 3 minutes             0.0.0.0:5555->5555/tcp, :::5555->5555/tcp   dials-flower
15d46df20bae   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 3 minutes                                                         dials-csc-priority
baf109de235d   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 3 minutes                                                         dials-egamma0-downloader-priority
3884c8f99f84   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 3 minutes                                                         dials-streamhiexpressrawprime-downloader-priority
684bf5b1c590   dials_backend    "python manage.py ru…"   3 minutes ago   Up 3 minutes             0.0.0.0:8000->8000/tcp, :::8000->8000/tcp   dials-backend
75129249fca6   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 3 minutes                                                         dials-jetmet-bulk
376651d7e7aa   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 3 minutes                                                         dials-common-indexer
037b8d76bd2b   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 3 minutes                                                         dials-jetmet0-downloader-priority
5457add93b70   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 3 minutes                                                         dials-egamma-priority
84d7579e8e55   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 3 minutes                                                         dials-ecal-priority
b5b8d8f77d9b   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 3 minutes                                                         dials-zerobias-downloader-bulk
a5c5c169ad25   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 3 minutes                                                         dials-beat-scheduler
641dfd7c783a   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 2 minutes                                                         dials-streamhiexpressrawprime-downloader-bulk
2f453412609f   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 3 minutes                                                         dials-muon-downloader-bulk
1ddefde9b55b   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 2 minutes                                                         dials-tracker-priority
a9a531ec4ba9   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 3 minutes                                                         dials-hcal-bulk
3501e2fa8e70   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 3 minutes                                                         dials-muon0-downloader-bulk
699d1be4d9a3   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 3 minutes                                                         dials-muon-downloader-priority
4d7e223b7223   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 3 minutes                                                         dials-jetmet0-downloader-bulk
44ae49dfd684   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 3 minutes                                                         dials-jetmet-downloader-bulk
ca2b173ac6ad   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 3 minutes                                                         dials-streamexpress-downloader-priority
991418bbb585   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 3 minutes                                                         dials-ecal-bulk
dc2ceb05851a   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 3 minutes                                                         dials-private-bulk
3559615921e2   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 3 minutes                                                         dials-hcal-priority
43564916c050   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 2 minutes                                                         dials-hiforward0-downloader-priority
47ffe85cca3b   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 3 minutes                                                         dials-hiphysicsrawprime0-downloader-bulk
dbeaf5400e28   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 3 minutes                                                         dials-egamma-bulk
cd74ea827db5   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 3 minutes                                                         dials-zerobias-downloader-priority
69cf337c5220   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 3 minutes                                                         dials-jetmet-priority
dc7a3eb6f4ac   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 3 minutes                                                         dials-tracker-bulk
550cfb344890   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 2 minutes                                                         dials-muon0-downloader-priority
13ff85cfafbc   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 3 minutes                                                         dials-egamma0-downloader-bulk
5ccc88160753   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 3 minutes                                                         dials-private-downloader-bulk
1b66144b6f90   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 3 minutes                                                         dials-hiforward0-downloader-bulk
f52544c371d6   dials_etl        "bash -c 'celery --a…"   3 minutes ago   Up 3 minutes                                                         dials-streamexpress-downloader-bulk
67b69b897c86   postgres         "docker-entrypoint.s…"   22 hours ago    Up 3 minutes (healthy)   0.0.0.0:5432->5432/tcp, :::5432->5432/tcp   postgresql-local
d429b32d6206   redis            "docker-entrypoint.s…"   22 hours ago    Up 3 minutes (healthy)   0.0.0.0:6379->6379/tcp, :::6379->6379/tcp   redis-local
```

### Interacting with the Docker container

#### Stopping the container

For killing all processes, use the ctrl+c keys.

#### Starting the data extraction process

In principle, the indexing, downloading and ingestion procedure is automatically launched at the start of every hour. However, for testing purposes, one can force the indexing by running the `trigger-indexing` script from inside the docker container with:

```bash
docker exec -it dials-flower bash -c 'python3 cli.py indexing -s'
```

#### Monitoring the queues

Tasks can be monitored trough flower.
Open a web browser and enter `localhost:5555` in the address bar.
The webpage will ask for a login, the default username and password for local development is `admin`.

#### Interacting with your local DIALS web interface

Open a web browser and enter `localhost:3000` in the address bar.

#### Interacting with your local DIALS API

Open a web browser and enter `localhost:8000` in the address bar.

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

#### Removing all generated containers

```bash
docker compose down
docker compose --profile=donotstart down
```

#### Removing all generated images

```bash
docker images dials\* -q | xargs docker rmi
```


## Building and running a local DIALS instance natively (i.e. without Docker)

### Setting up a local environment

The etl and backend uses `Python` `^3.10.13` , the third-party dependencies are managed by [`poetry`](https://python-poetry.org/) `^1.7.1` and note that explicitly the etl has a hard dependency on `ROOT` `^6.30/02`. After having all these dependencies you can run `poetry install --no-root` to install all the etl and backend dependencies specified in `pyproject.toml`. Then you should configure `pre-commit` by running `poetry run pre-commit install`, this will ensure code standardization.

The frontend uses `Node.js` `^20.11.0` and the third-party dependencies are managed by [`yarn`](https://www.npmjs.com/package/yarn) that can be installed using `npm install -g yarn`. Then you can run `yarn install` to install the frontend dependencies specified in `package.json`. Note that the frontend will not work if code does not agree with `eslint` configuration, to fix any style problems you can run `yarn run lint`.

Note: in case you will be using Docker, the above setup steps are not needed. On the other hand, you will need the `pyyaml` package to generate the docker compose file.

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
