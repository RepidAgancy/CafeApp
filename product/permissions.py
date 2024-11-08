from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions
from rest_framework.exceptions import ValidationError

from accounts import models

class IsStorekeeper(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and  request.user.type == models.STOREKEEPER:
            return True
        return False