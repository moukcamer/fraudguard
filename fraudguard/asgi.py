# fraudguard/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fraudguard.settings')

# Initialize Django ASGI app
django_asgi_app = get_asgi_application()

# Import WebSocket consumers after Django is ready
from apps.fraud_detection.consumers import FraudAlertConsumer

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                path("ws/fraud/alerts/", FraudAlertConsumer.as_asgi()),
            ])
        )
    ),
})