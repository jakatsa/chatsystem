import os
from urllib.parse import parse_qs
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.middleware import BaseMiddleware
from django.db import close_old_connections

from chatapp.routing import websocket_urlpatterns

# ✅ Set the Django settings module FIRST
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatsystemproj.settings')


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # ✅ All Django-related imports inside the method
        from django.contrib.auth import get_user_model
        from django.contrib.auth.models import AnonymousUser
        from rest_framework_simplejwt.tokens import AccessToken

        query_string = scope["query_string"].decode()
        query_params = parse_qs(query_string)
        token = query_params.get("token", [None])[0]

        if token:
            try:
                validated_token = AccessToken(token)
                user_id = validated_token["user_id"]
                User = get_user_model()
                user = await User.objects.aget(id=user_id)
                scope["user"] = user
            except Exception as e:
                print("JWT auth error:", e)
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()

        close_old_connections()
        return await super().__call__(scope, receive, send)

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    ),
})
