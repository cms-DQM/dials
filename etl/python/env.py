from decouple import Choices, Csv, config


class EnvChoices:
    dev = "dev"
    prod = "prod"

    @staticmethod
    def values():
        return [value for key, value in vars(EnvChoices).items() if not key.startswith("__") and isinstance(value, str)]


ENV = config("ENV", cast=Choices(EnvChoices.values()))
RAW_LAYERS = config("RAW_LAYERS", cast=Csv())
MODEL_REGISTRY_PATH = config("MODEL_REGISTRY_PATH")
DATABASE_RUI = config("DATABASE_URI")
GRID_CERT_FPATH = config("CERT_FPATH")
GRID_CERT_KEY_FPATH = config("KEY_FPATH")
CELERY_BROKER_URL = config("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND")
CELERY_REDBEAT_URL = config("CELERY_REDBEAT_URL")
MOCKED_DBS_FPATH = config("MOCKED_DBS_FPATH", default="")
ETL_CONFIG_FPATH = config("ETL_CONFIG_FPATH")
