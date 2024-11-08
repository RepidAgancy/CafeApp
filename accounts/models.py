from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

ADMIN, WAITER, CASHIER, STOREKEEPER = (_('admin'), _('afitsant'), _('kassir'), _('omborchi'))

class User(AbstractUser):
    USER_TYPE = (
        (ADMIN, ADMIN,),
        (WAITER, WAITER),
        (CASHIER, CASHIER),
        (STOREKEEPER, STOREKEEPER),
    )

    type = models.CharField(max_length=50, choices=USER_TYPE)

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
