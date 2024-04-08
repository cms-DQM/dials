from decouple import config


app_env = config("ENV")

eos_landing_zone = config("EOS_LANDING_ZONE")

mounted_eos_path = config("MOUNTED_EOS_PATH", default=None)

db_engine = config("DATABASE_ENGINE")
db_user = config("DATABASE_USER")
db_pwd = config("DATABASE_PASSWORD")
db_host = config("DATABASE_HOST")
db_port = config("DATABASE_PORT")
conn_str = f"{db_engine}://{db_user}:{db_pwd}@{db_host}:{db_port}"

lxplus_user = config("LXPLUS_USER")
lxplus_pwd = config("LXPLUS_PWD")

cert_fpath = config("CERT_FPATH")
key_fpath = config("KEY_FPATH")

celery_broker_url = config("CELERY_BROKER_URL")
celery_result_backend = config("CELERY_RESULT_BACKEND")
celery_redbeat_url = config("CELERY_REDBEAT_URL")

mocked_dbs_fpath = config("MOCKED_DBS_FPATH", default="")
