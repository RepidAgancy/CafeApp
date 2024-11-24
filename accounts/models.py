from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel
from accounts.utils import WebpImageField

ADMIN, WAITER, CASHIER, STOREKEEPER, COOKER = (_('admin'), _('ofitsant'), _('kassir'), _('omborchi'),_('oshpaz'))


class User(AbstractUser, BaseModel):
    USER_TYPE = (
        (ADMIN, ADMIN,),
        (WAITER, WAITER),
        (CASHIER, CASHIER),
        (STOREKEEPER, STOREKEEPER),
        (COOKER, COOKER)
    )
    type = models.CharField(max_length=50, choices=USER_TYPE)
    profile_image = WebpImageField(upload_to='accounts/images/profile/%Y/%m/%d/',null=True, blank=True)
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    work_experience = models.CharField(max_length=250)
    salary = models.PositiveIntegerField(default=0)

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    @classmethod
    def get_user_type_list(cls):
        return [choice[1] for choice in cls.USER_TYPE]

    def save(self, *args, **kwargs):
        if self.profile_image:
            # Ensure WebP conversion on save
            self.image = self.profile_image.file  # Access file object
        super().save(*args, **kwargs)

