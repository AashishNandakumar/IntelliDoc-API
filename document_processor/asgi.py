"""
ASGI config for document_processor project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "document_processor.settings")
django.setup()
django_asgi_app = (
    get_asgi_application()  # used to expose your existing django http views
)  # make sure this is done before any other external imports (daphne requires this)

import chat.routing

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": URLRouter(
            chat.routing.websocket_urlpatterns,
        ),
    }
)
