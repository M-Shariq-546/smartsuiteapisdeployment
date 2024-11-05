import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smartsuite.settings")
django.setup()  # Make sure Django is initialized first

from django.core.asgi import get_asgi_application
import group_chats.api.routing  # Import after setup

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            group_chats.api.routing.websocket_urlpatterns
        )
    ),
})
