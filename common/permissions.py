from rest_framework.permissions import BasePermission

from accounts import models

class IsWaiter(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.type == models.WAITER or request.user.profession.name_en == 'waiter':
            return True
        else:
            return False


class IsCashier(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.type == models.CASHIER or request.user.profession.name_en == 'cashier':
            return True
        else:
            return False
