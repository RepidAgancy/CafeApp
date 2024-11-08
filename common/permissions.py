from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import BasePermission

from accounts import models

class IsWaiter(BasePermission):
    def has_permission(self, request, view):
        # user = request.user
        # if isinstance(user, AnonymousUser):
        #     raise ValidationError('You are not logged in')
        if request.user.is_authenticated and request.user.type == models.WAITER:
            return True
        else:
            return False


class IsCashier(BasePermission):
    def has_permission(self, request, view):
        # user = request.user
        # if isinstance(user, AnonymousUser):
        #     raise ValidationError('You are not logged in')
        if request.user.is_authenticated and request.user.type == models.CASHIER:
            return True
        else:
            return False
