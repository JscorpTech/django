from config.settings.common import *  # noqa
from config.settings.common import ALLOWED_HOSTS, REST_FRAMEWORK

ALLOWED_HOSTS += []

REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {"user": "60/min"}
