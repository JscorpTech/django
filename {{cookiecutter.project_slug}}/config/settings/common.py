import importlib
import os
import pathlib
from typing import List, Union

from config.conf import *  # noqa
from config.conf.apps import APPS
from config.conf.modules import MODULES
from config.env import env
from django.utils.translation import gettext_lazy as _

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent

SECRET_KEY = env.str("DJANGO_SECRET_KEY")
DEBUG = env.bool("DEBUG")

ALLOWED_HOSTS: Union[List[str]] = ["*"]

DATABASES = {
    "default": {
        "ENGINE": env.str("DB_ENGINE"),
        "NAME": env.str("DB_NAME"),
        "USER": env.str("DB_USER"),
        "PASSWORD": env.str("DB_PASSWORD"),
        "HOST": env.str("DB_HOST"),
        "PORT": env.str("DB_PORT"),
    }
}

INSTALLED_APPS = [
                     "modeltranslation",
                     "unfold",
                     "unfold.contrib.filters",
                     "unfold.contrib.forms",
                     "unfold.contrib.guardian",
                     "unfold.contrib.simple_history",
                     "django.contrib.admin",
                     "django.contrib.auth",
                     "django.contrib.contenttypes",
                     "django.contrib.sessions",
                     "django.contrib.messages",
                     "django.contrib.staticfiles",
                 ] + APPS

MODULES = [app for app in MODULES if isinstance(app, str)]

for module_path in MODULES:
    INSTALLED_APPS.append("{}.apps.ModuleConfig".format(module_path))

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # Cors middleware
    "django.middleware.locale.LocaleMiddleware",  # Locale middleware
    "core.http.middlewares.CacheMiddleware",  # Cache middle
    *(
        ["django.middleware.cache.UpdateCacheMiddleware"]
        if env.bool("CACHE_ENABLED")
        else []
    ),  # Update cache middle
    "django.middleware.common.CommonMiddleware",
    *(
        ["django.middleware.cache.FetchFromCacheMiddleware"]
        if env.bool("CACHE_ENABLED")
        else []
    ),  # Fetch from cache middle
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "resources/templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
# fmt: off
{ % if cookiecutter.runner == 'asgi' %}
ASGI_APPLICATION = "config.asgi.application"
{ % else %}
WSGI_APPLICATION = "config.wsgi.application"
{ % endif %}
# fmt: on

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.{}".format(validator)
    } for validator in [
        "UserAttributeSimilarityValidator",
        "MinimumLengthValidator",
        "CommonPasswordValidator",
        "NumericPasswordValidator"
    ]
]

TIME_ZONE = "Asia/Tashkent"
USE_I18N = True
USE_TZ = True
STATIC_URL = "resources/static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Date formats
##
DATE_FORMAT = "d.m.y"
TIME_FORMAT = "H:i:s"
DATE_INPUT_FORMATS = ["%d.%m.%Y", "%Y.%d.%m", "%Y.%d.%m"]

SEEDERS = ["core.http.seeder.UserSeeder"]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "resources/static"),
]

CORS_ORIGIN_ALLOW_ALL = True

STATIC_ROOT = os.path.join(BASE_DIR, "resources/staticfiles")
VITE_APP_DIR = os.path.join(BASE_DIR, "resources/static/vite")

LANGUAGES = (
    ("ru", _("Russia")),
    ("en", _("English")),
    ("uz", _("Uzbek")),
)
LOCALE_PATHS = [os.path.join(BASE_DIR, "resources/locale")]

MODELTRANSLATION_LANGUAGES = ("uz", "ru", "en")
MODELTRANSLATION_DEFAULT_LANGUAGE = "uz"
LANGUAGE_CODE = "uz"

MEDIA_ROOT = os.path.join(BASE_DIR, "resources/media")  # Media files
MEDIA_URL = "/resources/media/"

AUTH_USER_MODEL = "http.User"

CELERY_BROKER_URL = env("RABBITMQ_URL")
CELERY_RESULT_BACKEND = env("RABBITMQ_RESULT_BACKEND")

ALLOWED_HOSTS += env("ALLOWED_HOSTS").split(",")
CSRF_TRUSTED_ORIGINS = env("CSRF_TRUSTED_ORIGINS").split(",")
