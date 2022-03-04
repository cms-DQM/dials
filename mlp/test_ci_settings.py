from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'testdb',
        'USER': 'travis',
        # 'HOST': 'localhost'
    }
}

DYNAMIC_PREFERENCES = {
    'ENABLE_CACHE': False,
}
