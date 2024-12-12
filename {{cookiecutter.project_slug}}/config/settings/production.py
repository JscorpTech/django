from config.settings.common import *  # noqa
from config.settings.common import ALLOWED_HOSTS, REST_FRAMEWORK

ALLOWED_HOSTS += ["192.168.100.26", "80.90.178.156"]

REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {"user": "60/min"}
