# MLPlayground

## Components

* DQMIO File Indexer (DFI)
* DQMIO ETL (DETL)

### DFI

Component responsible for keeping track of data (DQMIO rootfiles) stored in EOS using a database table. It should store files metadata (run number, primary dataset, ...), filepath in EOS filesystem, processing status and some statistics. We must provide automatic updates to our knowledge base and offer a button to let a user trigger the indexer on-demand. In or to snure that no duplicated threads exists each processing will happen one at a time using a job queue.

### DETL

Component responsible for executing our ETL (Extract-Transform-Load) pipeline based on files not yet processed stored by DFI. Given the fact that DQMIO files vary in size, it is not possible to forecast how much computer resources would be enough for processing multiple files at the sime time, then the processing will happen one at a time using a job queue.

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
