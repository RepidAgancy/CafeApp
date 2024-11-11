from django.urls import path

from .consumer import RoomConsumer

websocket_urlpatterns = [
    path('ws/chat/', RoomConsumer.as_asgi()),
]
