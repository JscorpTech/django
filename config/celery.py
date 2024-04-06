#####################
# Celery settings
#####################

from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from django.conf import settings

from common.env import env

os.environ.setdefault('DJANGO_SETTINGS_MODULE', env("DJANGO_SETTINGS_MODULE"))

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
