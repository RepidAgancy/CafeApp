from rest_framework.permissions import BasePermission

from accounts.models import ADMIN

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.type == ADMIN:
            return True
        return False