from .consumers import ChatConsumer
from django.urls import re_path


urlpatterns = [
    re_path(r'ws/chat/$', ChatConsumer.as_asgi()),

]
