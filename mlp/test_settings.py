from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db_extended.sqlite3',
    }
}

DYNAMIC_PREFERENCES = {
    'ENABLE_CACHE': False,
}