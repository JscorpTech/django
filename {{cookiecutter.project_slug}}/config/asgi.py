import os

from django.core.asgi import get_asgi_application

asgi_application = get_asgi_application()
from config.env import env  # noqa

os.environ.setdefault("DJANGO_SETTINGS_MODULE", env("DJANGO_SETTINGS_MODULE"))

{% if cookiecutter.channels %}
from channels.routing import ProtocolTypeRouter  # noqa
from channels.routing import URLRouter  # noqa
# from core.apps.websocket.urls import websocket_urlpatterns  # noqa
# from core.apps.websocket.middlewares import JWTAuthMiddlewareStack  # noqa

application = ProtocolTypeRouter(
    {
        "http": asgi_application,
        # "websocket": JWTAuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
{% else %}
application = asgi_application()
{% endif %}
