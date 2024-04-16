#!/usr/bin/env python

import os
import sys


sys.path.insert(0, os.getcwd())

from python.config import workspaces
from python.env import conn_str
from python.models import DQMIOIndex
from python.pipelines.indexer.methods import post_load
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


dm_name = sys.argv[1]
files_ids = sys.argv[2].split(",")

engine = create_engine(f"{conn_str}/{dm_name}")
workspace = next(filter(lambda x: x["name"] == dm_name, workspaces))

session = sessionmaker(bind=engine)
with session() as sess:
    query = sess.query(DQMIOIndex).filter(DQMIOIndex.file_id.in_(files_ids))
    results = query.all()
    results = [{k: v for k, v in result.__dict__.items() if k != "_sa_instance_state"} for result in results]

post_load(engine, workspace, inserted_files=results)
