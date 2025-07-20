import django

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot.settings')
django.setup()
from core import routing

application = ProtocolTypeRouter({
   "http": get_asgi_application(),
   "websocket": URLRouter(
      routing.websocket_urlpatterns
   ),
})