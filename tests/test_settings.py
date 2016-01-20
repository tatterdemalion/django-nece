import os

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), os.pardir)

SECRET_KEY = 'not_so_secret_r2fetCebUAZB3DhzTn5NPg8J08IancuGt04npTMh'
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nece',
        'USER': 'postgres',
    }
}

INSTALLED_APPS = ('nece', 'tests',)
TRANSLATIONS_DEFAULT = 'en_us'
TRANSLATIONS_MAP = {'en': 'en_us', 'tr': 'tr_tr', 'de': 'de_de', 'it': 'it_it'}
