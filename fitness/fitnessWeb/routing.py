# from email.mime import application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.urls import path
# from chat.consumers import EchoConsumer

# application = ProtocolTypeRouter({
#     'websocket': URLRouter([
#         path('ws/chat/', EchoConsumer)
#     ])
# })

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [  
    re_path(r'ws/socket-server/', consumers.ChatConsumer.as_asgi())
]