from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel

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
    profile_image = models.ImageField(upload_to='accounts/images/',null=True, blank=True)
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
            image = Image.open(self.profile_image)
            image = image.convert("RGB")
            max_size = (1024, 1024)
            image.thumbnail(max_size, Image.Resampling.LANCZOS)

            buffer = BytesIO()
            image.save(buffer, format='WEBP', quality=80, optimize=True)
            buffer.seek(0)

            new_image_name = f"{self.profile_image.name.split('.')[0]}.webp"
            self.profile_image.save(
                new_image_name,
                ContentFile(buffer.read()),
                save=False
            )

        super().save(*args, **kwargs)
