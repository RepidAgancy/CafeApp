from django.db import models
from django.contrib.auth.models import AbstractUser

ADMIN, WAITER, CASHIER, STOREKEEPER = ('admin', 'afitsant', 'kassir', 'omborchi')

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
