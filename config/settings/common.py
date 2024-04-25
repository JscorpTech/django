import os
import pathlib
from django.utils.translation import gettext_lazy as _

from common.env import env
from config.conf import *  # noqa

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent

SECRET_KEY = env.str("DJANGO_SECRET_KEY")
DEBUG = env.str("DEBUG")

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    # Design admin panel
    "jazzmin",
    "django_select2",
    "modeltranslation",

    # Default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INSTALLED_APPS += apps.INSTALLED_APPS  # noqa

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    "corsheaders.middleware.CorsMiddleware",  # Cors middleware
    "django.middleware.locale.LocaleMiddleware",  # Locale middleware
    "core.middlewares.cache_middleware.CacheMiddleware",  # Cache middle

    *(['django.middleware.cache.UpdateCacheMiddleware']
      if env.bool("CACHE_ENABLED") else []),  # Update cache middle
    'django.middleware.common.CommonMiddleware',

    *(['django.middleware.cache.FetchFromCacheMiddleware']
      if env.bool("CACHE_ENABLED") else []),  # Fetch from cache middle

    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'routes'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "resources/templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.NumericPasswordValidator',
    },
]

TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Date formats
##
DATE_FORMAT = "d.m.y"
TIME_FORMAT = 'H:i:s'
DATE_INPUT_FORMATS = ['%d.%m.%Y', "%Y.%d.%m", "%Y.%d.%m"]

FACTORYS = [
    ("core.http.database.factory.PostFactory", 100000),
    # ("core.http.database.factory.UserFactory", 1),
]

SEEDERS = [
    "core.http.database.seeder.UserSeeder"
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "resources/static"),
]

CORS_ORIGIN_ALLOW_ALL = True

PAYCOM_SETTINGS = {
    "KASSA_ID": "1111",
    "ACCOUNTS": {
        "KEY": "1234",
    },
    "TOKEN": "1111"
}

STATIC_ROOT = os.path.join(BASE_DIR, "resources/staticfiles")
VITE_APP_DIR = os.path.join(BASE_DIR, "resources/static/vite")

LANGUAGES = (
    ('ru', _('Russia')),
    ('en', _('English')),
    ('uz', _('Uzbek')),
)
LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale")
]

MODELTRANSLATION_LANGUAGES = ("uz", "ru", "en")
MODELTRANSLATION_DEFAULT_LANGUAGE = "uz"
LANGUAGE_CODE = 'uz'

MEDIA_ROOT = os.path.join(BASE_DIR, "media")  # Media files
MEDIA_URL = '/media/'

AUTH_USER_MODEL = 'http.User'

CELERY_BROKER_URL = env("REDIS_URL")
CELERY_RESULT_BACKEND = env("REDIS_URL")

CRISPY_TEMPLATE_PACK = 'tailwind'

ALLOWED_HOSTS += env("ALLOWED_HOSTS").split(",")
CSRF_TRUSTED_ORIGINS = env("CSRF_TRUSTED_ORIGINS").split(",")
