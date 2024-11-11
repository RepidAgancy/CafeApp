from django.urls import path

from .views import RoomCreateAPIView

urlpatterns = [
    path('create-room', RoomCreateAPIView.as_view()),
]