from decouple import config


app_env = config("ENV")
mounted_eos_path = config("MOUNTED_EOS_PATH")
model_registry_path = config("MODEL_REGISTRY_PATH")
conn_str = config("DATABASE_URI")
cert_fpath = config("CERT_FPATH")
key_fpath = config("KEY_FPATH")
celery_broker_url = config("CELERY_BROKER_URL")
celery_result_backend = config("CELERY_RESULT_BACKEND")
celery_redbeat_url = config("CELERY_REDBEAT_URL")
mocked_dbs_fpath = config("MOCKED_DBS_FPATH", default="")
etl_config_fpath = config("ETL_CONFIG_FPATH")
