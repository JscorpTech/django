import os
import pathlib
from typing import List, Union, Iterable

from django.utils.translation import gettext_lazy as _
from core.utils import Config
from config.conf import *  # noqa
from config.env import env
from config.conf.apps import APPS
import importlib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent

SECRET_KEY = env.str("DJANGO_SECRET_KEY")
DEBUG = env.str("DEBUG")

ALLOWED_HOSTS: Union[List[str]] = ["*"]

INSTALLED_APPS = [
    "daphne",
    # Design admin panel
    "django_select2",
    "modeltranslation",
    # Django unfold
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    # "unfold.contrib.inlines",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history",
    # End Django unfold
    # Default apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

apps: Iterable[str] = Config().config.get("modules") or []

MODULES = [f"core.apps.{app}" for app in apps if isinstance(app, str)]
INSTALLED_APPS += APPS

for module_path in MODULES:
    INSTALLED_APPS.append("{}.apps.ModuleConfig".format(module_path))
    module = importlib.import_module(module_path)
    module_dict = module.__dict__
    globals().update({k: v for k, v in module_dict.items() if not k.startswith('__')})

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # Cors middleware
    "django.middleware.locale.LocaleMiddleware",  # Locale middleware
    "core.middlewares.CacheMiddleware",  # Cache middle
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

ROOT_URLCONF = "routes"

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

# WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation"
        ".UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".NumericPasswordValidator",
    },
]

TIME_ZONE = "Asia/Tashkent"
USE_I18N = True
USE_TZ = True
STATIC_URL = "resource/static/"
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

PAYCOM_SETTINGS = {
    "KASSA_ID": "1111",
    "ACCOUNTS": {
        "KEY": "1234",
    },
    "TOKEN": "1111",
}

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

CRISPY_TEMPLATE_PACK = "tailwind"

ALLOWED_HOSTS += env("ALLOWED_HOSTS").split(",")
CSRF_TRUSTED_ORIGINS = env("CSRF_TRUSTED_ORIGINS").split(",")
