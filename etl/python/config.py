import json
import os.path

from .env import ETL_CONFIG_FPATH


# If etl config file path is specific but dot no exists, stop the program
if os.path.exists(ETL_CONFIG_FPATH) is False:
    raise Exception("etl config file not found in specified path.")

# Read configuration from object
with open(ETL_CONFIG_FPATH) as f:
    config_contents = json.load(f)

# Expose objects
COMMON_CHUK_SIZE = config_contents["common_chunk_size"]
COMMON_INDEXER_QUEUE = config_contents["common_indexer_queue"]
DEV_ENV_LABEL = config_contents["dev_env_label"]
PRIORITY_ERA = config_contents["priority_era"]
TH1_TYPES = config_contents["th1_types"]
TH2_TYPES = config_contents["th2_types"]
TH2_CHUNK_SIZE = config_contents["th2_chunk_size"]
WORKSPACES = config_contents["workspaces"]

# List all primary datasets (removing duplicates)
PRIMARY_DATASETS = [obj for ws in WORKSPACES for obj in ws["primary_datasets"]]
PRIMARY_DATASETS = {(d["dbs_pattern"], d["dbs_instance"]): d for d in PRIMARY_DATASETS}.values()
PRIMARY_DATASETS = sorted(PRIMARY_DATASETS, key=lambda x: x["dbs_pattern"])

# We can delete config_contents from memory
del config_contents
