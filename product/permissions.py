from rest_framework import permissions

from accounts import models

class IsStorekeeper(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.type == models.STOREKEEPER:
                return True
        return False