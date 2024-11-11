from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel

ADMIN, WAITER, CASHIER, STOREKEEPER = (_('admin'), _('afitsant'), _('kassir'), _('omborchi'))


class User(AbstractUser, BaseModel):
    USER_TYPE = (
        (ADMIN, ADMIN,),
        (WAITER, WAITER),
        (CASHIER, CASHIER),
        (STOREKEEPER, STOREKEEPER),
    )
    profession = models.CharField(max_length=50)
    type = models.CharField(max_length=50, choices=USER_TYPE)
    profile_image = models.ImageField(upload_to='accounts/images/profile/%Y/%m/%d/')
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    work_experience = models.CharField(max_length=250)
    salary = models.PositiveIntegerField(default=0)

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    @classmethod
    def get_user_type_list(cls):
        return [choice[1] for choice in cls.USER_TYPE]


