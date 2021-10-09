from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from social.routing import websockets_urls

application = ProtocolTypeRouter({
    'websockets': AuthMiddlewareStack(
        URLRouter(
            websockets_urls
        )
    )
})