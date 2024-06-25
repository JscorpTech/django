import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
from core.middlewares import JWTAuthMiddlewareStack
from channels.routing import URLRouter
from core.apps.home.websocket.routing import urlpatterns

from config.env import env

os.environ.setdefault("DJANGO_SETTINGS_MODULE", env("DJANGO_SETTINGS_MODULE"))


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": JWTAuthMiddlewareStack(URLRouter(urlpatterns)),
    }
)
