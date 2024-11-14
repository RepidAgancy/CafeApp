from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import RoomCreateSerializer, UserSerializer
from .models import Room
from accounts.models import User

class RoomCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RoomCreateSerializer
    queryset = Room.objects.all()


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer