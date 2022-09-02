"""
ASGI config for fitness project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
from typing import Protocol

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import fitnessWeb.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness.settings')

application = ProtocolTypeRouter ({
    'http' : get_asgi_application(),
    'websocket' : AuthMiddlewareStack(
        URLRouter(
            fitnessWeb.routing.websocket_urlpatterns
        )
    )
})
