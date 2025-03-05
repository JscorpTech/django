import os
import pathlib
from typing import List, Union

from config.conf import *  # noqa
from config.conf.apps import APPS
from config.conf.modules import MODULES
from config.env import env
from django.utils.translation import gettext_lazy as _
from rich.traceback import install

install(show_locals=True)
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent

SECRET_KEY = env.str("DJANGO_SECRET_KEY")
DEBUG = env.bool("DEBUG")

ALLOWED_HOSTS: Union[List[str]] = ["*"]

if env.bool("PROTOCOL_HTTPS", False):
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

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

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.BCryptPasswordHasher",
]

INSTALLED_APPS = [
    {% if cookiecutter.modeltranslation %}"modeltranslation",{% endif %}
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
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
if env.str("PROJECT_ENV") == "debug":
    MIDDLEWARE += [
        {% if cookiecutter.silk %}"silk.middleware.SilkyMiddleware",{% endif %}
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
{% if cookiecutter.runner == 'asgi' %}
ASGI_APPLICATION = "config.asgi.application"
{% else %}
WSGI_APPLICATION = "config.wsgi.application"
{% endif %}
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


SEEDERS = ["core.apps.accounts.seeder.UserSeeder"]

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




LANGUAGE_CODE = "uz"

MEDIA_ROOT = os.path.join(BASE_DIR, "resources/media")  # Media files
MEDIA_URL = "/resources/media/"

AUTH_USER_MODEL = "accounts.User"

CELERY_BROKER_URL = env("RABBITMQ_URL")
CELERY_RESULT_BACKEND = env("RABBITMQ_RESULT_BACKEND")

ALLOWED_HOSTS += env("ALLOWED_HOSTS").split(",")
CSRF_TRUSTED_ORIGINS = env("CSRF_TRUSTED_ORIGINS").split(",")
{% if cookiecutter.silk %}SILKY_AUTHORISATION = True
SILKY_PYTHON_PROFILER = True{% endif %}
{% if cookiecutter.modeltranslation %}
MODELTRANSLATION_LANGUAGES = ("uz", "ru", "en")
MODELTRANSLATION_DEFAULT_LANGUAGE = "uz"{% endif %}
{% if cookiecutter.parler %}
PARLER_LANGUAGES = {
    None: (
        {'code': 'uz',},
        {'code': 'en',},
        {'code': 'ru',},
    ),
    'default': {
        'fallbacks': ['uz'],          # defaults to PARLER_DEFAULT_LANGUAGE_CODE
        'hide_untranslated': False,   # the default; let .active_translations() return fallbacks too.
    }
}{% endif %}


JST_LANGUAGES = [
    {
        "code": "uz",
        "name": "Uzbek",
        "is_default": True,
    },
    {
        "code": "en",
        "name": "English",
    },
    {
        "code": "ru",
        "name": "Russia",
    }
]
