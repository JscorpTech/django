from common.env import env
from config.settings.common import *  # noqa
from config.settings.common import MIDDLEWARE, ALLOWED_HOSTS, REST_FRAMEWORK


DATABASES = {
    "default": {
        "ENGINE": env("DB_ENGINE"),
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}

MIDDLEWARE += []

ALLOWED_HOSTS += ["192.168.100.26", "80.90.178.156"]

REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {
    "user": "10/min",
}
