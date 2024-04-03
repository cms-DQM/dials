from decouple import config


app_env = config("ENV")

files_landing_dir = config("FILES_LANDING_DIR")

db_engine = config("DATABASE_ENGINE")
db_user = config("DATABASE_USER")
db_pwd = config("DATABASE_PASSWORD")
db_host = config("DATABASE_HOST")
db_port = config("DATABASE_PORT")
conn_str = f"{db_engine}://{db_user}:{db_pwd}@{db_host}:{db_port}"

lxplus_user = config("LXPLUS_USER")
lxplus_pwd = config("LXPLUS_PWD")

sa_globus_path = config("SA_GLOBUS_PATH")

celery_broker_url = config("CELERY_BROKER_URL")
celery_result_backend = config("CELERY_RESULT_BACKEND")

mocked_dbs_fpath = config("MOCKED_DBS_FPATH", default="")
