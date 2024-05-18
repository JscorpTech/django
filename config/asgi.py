import os

from django.core.asgi import get_asgi_application

from common.env import env

os.environ.setdefault("DJANGO_SETTINGS_MODULE", env("DJANGO_SETTINGS_MODULE"))

application = get_asgi_application()
