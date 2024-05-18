from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from . import consumers
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r"chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
    re_path(r"online_users/$", consumers.OnlineUsersConsumer.as_asgi()),
]

