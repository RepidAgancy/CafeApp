from rest_framework import permissions

from accounts import models

class IsStorekeeper(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and  request.user.type == models.STOREKEEPER or request.user.profession.name_en == 'storekeeper':
            return True
        return False