# Local development

Documentation, tips and tricks to develop MLPlayground locally.

## Accessing DQMIO MLPlayground data from EOS

The following commands will mount the specific DQMIO production data from EOS in read-only mode in your home folder (if you don't like the location you can change it):

```bash
mkdir -p $HOME/data_mlplayground_dqmio
sshfs -o default_permissions,ro $USER@lxplus.cern.ch:/eos/project/m/mlplayground/public/DQMIO $HOME/data_mlplayground_dqmio
```

You can try running the application to ingest data from the production source, but given EOS limitations and network limitation it is much simpler to copy some files (20 is enough) to a local directory and use that as the data source for the local application.

In case you need to unmount (turning off the computer/losing connection to lxplus will umount automatically) you can run the following command:

```bash
umount $HOME/data_mlplayground_dqmio
```

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

## Running Celery Workers

Job queues need workers for collecting tasks from the queue, executing then and later acknowledge the task. Since we are running three queues, the following commands will spawn workers for then, given their specification.

```bash
celery -A mlplayground worker -l INFO -c 1 -n worker1 -Q dqmio_file_indexer_queue
celery -A mlplayground worker -l INFO -c 1 -n worker2 -Q dqmio_etl_queue
celery -A mlplayground worker -l INFO -c 4 -n worker3 -Q celery_periodic
```

## Running Celery Beat

Some tasks must be periodic, that is, execute in a specific time continuously. In a common UNIX like environment you would normally use CRON, here since we are already using Celery for managing our job queues it is much easier (and flexible) to use celery's beat scheduler.

```bash
celery -A mlplayground beat -l INFO
```

## Running django

Just using the simplest runserver you can start de development django server:

```bash
python manage.py runserver 0.0.0.0:8000
```

## Starting the backend natively

From within [`backend`](/backend/) you can use the [`start-dev.sh`](/backend/scripts/start-dev.sh) script or the poe task `poe start-dev` to start the entire backend stack in one command.

Note: If running the commands separated you should execute then inside the [`backend/mlplayground`](/backend/mlplayground/) directory.

## Starting the frontend natively

Inside the [`frontend`](/frontend/) directory you can using the script `yarn run start` to start the react-scripts development server.

## Starting backend and frontend using Docker

Both the [`backend`](/backend/) and [`frontend`](/frontend/) ships a `Dockerfile` that can be used for local development. Using the [`docker-compose.yaml`](/docker-compose.yaml) (be sure to read the notes at file's beginning) you can start both services by first building and then starting from the [repository root's directory](/):

```bash
docker compose build
docker compose up
```

You will notice that the docker compose file is set to bind-mount the code from backend and frontend in the host, so hot reloading works (i.e. you don't need to always build the container upon any modification)!!! In order to this work correctly you need to setup the current user GID and UID when building the container, **generally** UID and GID for single not-hardcore linux user are set to 1000 and both Dockerfiles use that as default values. In case you use a different UID/GID you can set then as build args:

```bash
docker compose build --build-arg UID=$(id -u) --build-arg GID=$(id -g)
```

Note that we are not using the `-d` flag for running then detached from the current terminal, that is a good idea for development sessions and since we are not specifying any docker compose file it is automatically choosing the base file.

## Simulating production

Production environment can be simulated using [`docker-compose.prod.yaml`](/docker-compose.prod.yaml), you just need to set right production environment variables and build and spin up the container pointing to the correct yaml file:

```bash
docker compose -f docker-compose.prod.yaml build
docker compose -f docker-compose.prod.yaml up
```

Differently from the local development yaml file, it doesn't bind-mount files from the container so you always need to rebuild the containers upon any modification and the commands/docker images are different.
