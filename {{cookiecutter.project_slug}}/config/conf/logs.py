import os
from pathlib import Path
import logging

BASE_DIR = Path(__file__).resolve().parent.parent.parent

LOG_DIR = BASE_DIR / "resources/logs"
os.makedirs(LOG_DIR, exist_ok=True)


class ExcludeErrorsFilter:
    def filter(self, record):
        return record.levelno <= logging.ERROR


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s %(name)s %(levelname)s %(filename)s:%(lineno)d - %(message)s",
        },
    },
    "filters": {
        "exclude_errors": {
            "()": ExcludeErrorsFilter,
        },
    },
    "handlers": {
        "daily_rotating_file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": LOG_DIR / "django.log",
            "when": "midnight",
            "backupCount": 30,
            "formatter": "verbose",
            "filters": ["exclude_errors"],
        },
        "error_file": {
            "level": "ERROR",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": LOG_DIR / "django_error.log",
            "when": "midnight",
            "backupCount": 30,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["daily_rotating_file", "error_file"],
            "level": "INFO",
            "propagate": True,
        },
        "root": {
            "handlers": ["daily_rotating_file", "error_file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}
