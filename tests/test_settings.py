import os
import dj_database_url

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), os.pardir)

SECRET_KEY = 'not_so_secret_r2fetCebUAZB3DhzTn5NPg8J08IancuGt04npTMh'
DEBUG = True

db_url = os.environ.get("DATABASE_URL",
                        "postgres://postgres@127.0.0.1/django_nece_test")
DB = dj_database_url.parse(db_url)

DATABASES = {
    'default': DB
}

INSTALLED_APPS = ('nece', 'tests',)
TRANSLATIONS_DEFAULT = 'en_us'
TRANSLATIONS_MAP = {'en': 'en_us', 'tr': 'tr_tr', 'de': 'de_de', 'it': 'it_it'}
TRANSLATIONS_FALLBACK = {'fr_ca': ['fr_fr'], 'en_us': ['en_gb']}
