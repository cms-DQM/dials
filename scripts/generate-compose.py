#!/usr/bin/env python

import json
import os
import re

import yaml
from decouple import Config, RepositoryEnv


def gen_common_depends_on():
    return {"dials-init": {"condition": "service_completed_successfully"}}


def gen_volumes(mounted_eos_path):
    volumes = ["./etl/:/home/app/etl"]
    if mounted_eos_path:
        # Docker gives the full path to the mounted volume
        # "error while creating mount source path"
        # when we try to mount the full path,
        # In any case we need to mount the root of the volume
        # because there are two mounts on the same root volume
        second_to_last_mount = "/".join(mounted_eos_path.split("/")[:2])
        volumes.append(f"{second_to_last_mount}:{second_to_last_mount}")
    return volumes


def gen_compose_header(mounted_eos_path):
    return {
        "services": {
            "dials-init": {
                "container_name": "dials-init",
                "image": "dials_etl",
                "build": {
                    "dockerfile": "etl/Dockerfile",
                    "context": ".",
                    "args": ["UID", "GID"],
                },
                "volumes": gen_volumes(mounted_eos_path),
                "command": "bash -c 'alembic upgrade head'",
                "network_mode": "host",
            },
            "dials-purge": {
                "container_name": "dials-purge",
                "image": "dials_etl",
                "build": {
                    "dockerfile": "etl/Dockerfile",
                    "context": ".",
                    "args": ["UID", "GID"],
                },
                "volumes": gen_volumes(mounted_eos_path),
                "command": "bash -c 'alembic downgrade -1'",
                "network_mode": "host",
                "profiles": ["donotstart"],
            },
            "dials-beat-scheduler": {
                "container_name": "dials-beat-scheduler",
                "image": "dials_etl",
                "volumes": gen_volumes(mounted_eos_path),
                "command": "bash -c 'celery --app=python beat --loglevel=INFO -S redbeat.RedBeatScheduler'",
                "network_mode": "host",
                "depends_on": gen_common_depends_on(),
            },
            "dials-common-indexer": {
                "container_name": "dials-common-indexer",
                "image": "dials_etl",
                "volumes": gen_volumes(mounted_eos_path),
                "command": "bash -c 'celery --app=python worker --loglevel=INFO --concurrency=1 --autoscale=1,0 --max-tasks-per-child=1 --hostname=common-indexer@%h --queues=common-indexer'",
                "network_mode": "host",
                "depends_on": gen_common_depends_on(),
            },
            "dials-backend": {
                "container_name": "dials-backend",
                "image": "dials_backend",
                "build": {
                    "dockerfile": "backend/Dockerfile",
                    "context": ".",
                    "args": ["UID", "GID"],
                },
                "volumes": ["./backend/:/home/app/backend"],
                "command": "python manage.py runserver 0.0.0.0:8000",
                "network_mode": "host",
                "depends_on": gen_common_depends_on(),
            },
            "dials-frontend": {
                "container_name": "dials-frontend",
                "image": "dials_frontend",
                "build": {
                    "dockerfile": "frontend/Dockerfile",
                    "context": ".",
                    "args": ["UID", "GID"],
                },
                "network_mode": "host",
                "depends_on": gen_common_depends_on(),
            },
            "flower": {
                "container_name": "dials-flower",
                "image": "dials_etl",
                "volumes": gen_volumes(mounted_eos_path),
                "command": "bash -c 'celery --app=python flower'",
                "network_mode": "host",
                "depends_on": gen_common_depends_on(),
                "environment": {"FLOWER_BASIC_AUTH": "admin:admin"},
            },
        }
    }


def gen_compose_workspace_workers(mounted_eos_path, db_name):
    return {
        f"dials-{db_name}-bulk": {
            "container_name": f"dials-{db_name}-bulk",
            "image": "dials_etl",
            "volumes": gen_volumes(mounted_eos_path),
            "command": f"bash -c 'celery --app=python worker --loglevel=INFO --concurrency=1 --autoscale=1,0 --max-tasks-per-child=1 --hostname={db_name}-bulk@%h --queues={db_name}-bulk'",
            "network_mode": "host",
            "depends_on": gen_common_depends_on(),
        },
        f"dials-{db_name}-priority": {
            "container_name": f"dials-{db_name}-priority",
            "image": "dials_etl",
            "volumes": gen_volumes(mounted_eos_path),
            "command": f"bash -c 'celery --app=python worker --loglevel=INFO --concurrency=1 --autoscale=1,0 --max-tasks-per-child=1 --hostname={db_name}-priority@%h --queues={db_name}-priority'",
            "network_mode": "host",
            "depends_on": gen_common_depends_on(),
        },
    }


def gen_compose_downloader_workers(mounted_eos_path, pd_name):
    return {
        f"dials-{pd_name.lower()}-downloader-bulk": {
            "container_name": f"dials-{pd_name.lower()}-downloader-bulk",
            "image": "dials_etl",
            "volumes": gen_volumes(mounted_eos_path),
            "command": f"bash -c 'celery --app=python worker --loglevel=INFO --concurrency=1 --autoscale=1,0 --max-tasks-per-child=1 --hostname={pd_name}-downloader-bulk@%h --queues={pd_name}-downloader-bulk'",
            "network_mode": "host",
            "depends_on": gen_common_depends_on(),
        },
        f"dials-{pd_name.lower()}-downloader-priority": {
            "container_name": f"dials-{pd_name.lower()}-downloader-priority",
            "image": "dials_etl",
            "volumes": gen_volumes(mounted_eos_path),
            "command": f"bash -c 'celery --app=python worker --loglevel=INFO --concurrency=1 --autoscale=1,0 --max-tasks-per-child=1 --hostname={pd_name}-downloader-priority@%h --queues={pd_name}-downloader-priority'",
            "network_mode": "host",
            "depends_on": gen_common_depends_on(),
        },
    }


if __name__ == "__main__":
    cwd = os.getcwd()
    if os.path.basename(cwd) != "dials":
        raise Exception(f"Expected to be in dials directory, but got {cwd}")

    config = Config(RepositoryEnv(f"{cwd}/etl/.env"))
    mounted_eos_path = config.get("MOUNTED_EOS_PATH")
    databases = config.get("DATABASES")
    etl_config_fpath = config("ETL_CONFIG_FPATH")
    databases = re.sub("\s+", "", databases).split(",")
    with open(etl_config_fpath) as f:
        primary_datasets = [elem for ws in json.load(f)["workspaces"] for elem in ws["primary_datasets"]]
        primary_datasets = sorted(set(primary_datasets))

    comments = """# Notes
#
# 1. This docker-compose is not production-ready, you should use it only for development purposes
#    if do not want to run the entire stack natively
#
# 2. This file assumes that PostgreSQL and Redis are running as standalone docker containers
#    as describe in backend's README, so we need to set network_mode to "host"
#    in any application that need to communicate with those containers.
#    Optionally you can modify it yourself an run PostgresSQL and Redis from it and remove the network_mode
#    but make sure to expose all the necessary ports and check the links between containers
"""

    docker_compose = gen_compose_header(mounted_eos_path)

    for db_name in databases:
        services = gen_compose_workspace_workers(mounted_eos_path, db_name)
        docker_compose["services"].update(services)

    for pd_name in primary_datasets:
        services = gen_compose_downloader_workers(mounted_eos_path, pd_name)
        docker_compose["services"].update(services)

    with open("docker-compose.yaml", "w") as f:
        f.write(comments + "\n")
        yaml.dump(docker_compose, f)
