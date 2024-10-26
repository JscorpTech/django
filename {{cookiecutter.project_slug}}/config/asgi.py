import os

from django.core.asgi import get_asgi_application

asgi_application = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter  # noqa

from config.env import env  # noqa

# from core.apps.websocket.urls import websocket_urlpatterns  # noqa
# from core.apps.websocket.middlewares import JWTAuthMiddlewareStack  # noqa

os.environ.setdefault("DJANGO_SETTINGS_MODULE", env("DJANGO_SETTINGS_MODULE"))


application = ProtocolTypeRouter(
    {
        "http": asgi_application,
        # "websocket": JWTAuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
