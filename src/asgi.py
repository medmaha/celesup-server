import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

from api.routes.messenging import websocket as websocketMessage
from api.routes.dashboard.posts import websocket as websocketPosts
from api.routes.master import websocket as websocketMaster

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")


routes = [
    *websocketPosts.post_ws_urlpatterns,
    *websocketMessage.message_ws_urlpatterns,
    *websocketMaster.master_ws_urlpatterns,
]

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(routes))
        ),
    }
)
