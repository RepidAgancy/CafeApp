from rest_framework.permissions import BasePermission

from accounts import models

class IsWaiter(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.type == models.WAITER:
            return True
        else:
            return False
