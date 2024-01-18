# MLPlayground

## Components

* DQMIO File Indexer (DFI)
* DQMIO ETL (DETL)
* DQMIO Data-visualizer (DDV)

### DFI

Component responsible for keeping track of data (DQMIO rootfiles) stored in EOS using a database table. It should store files metadata (run number, primary dataset, ...), filepath in EOS filesystem, processing status and some statistics. We must provide automatic updates to our knowledge base and offer a button to let a user trigger the indexer on-demand.

NOTE: the indexer should be executed only one at a given time, so a job queue must be used to ensure no duplicated threads exists.

### DETL

Component responsible for executing our ETL (Extract-Transform-Load) pipeline based on files not yet processed stored by DDI.

NOTE: as some DQMIO files can be big, we will also need a job queue to limit how many pipelines can run parallelly in background.

### DDV

Component responsible for reading data processed by DETL and rendering histograms.


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

Considering the main application will only communicate with the database using PostgreSQL DBMS (i.e. not messing with database files directly), running the DBMS decoupled from the main application is less stressful and simulates the production environment. It goes without saying that is much easier to run Postgres using Docker and using the `-v` flag we can bind-mount the data stored inside the container in the host in order to have a persitent database accross development sessions.

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
docker run -d --name redis_local -p 6379:6379 redis
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
