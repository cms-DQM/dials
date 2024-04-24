#!/usr/bin/env python

import os
import sys


sys.path.insert(0, os.getcwd())

from python.config import common_indexer_queue, primary_datasets, workspaces
from python.pipelines.dataset_indexer.tasks import dataset_indexer_pipeline_task


dataset_indexer_pipeline_task.apply_async(
    kwargs={"workspaces": workspaces, "primary_datasets": primary_datasets}, queue=common_indexer_queue
)
