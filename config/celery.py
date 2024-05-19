"""
Celery configurations
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import os
import celery
from django.conf import settings

from common.env import env

os.environ.setdefault("DJANGO_SETTINGS_MODULE", env("DJANGO_SETTINGS_MODULE"))

app = celery.Celery("config")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
