from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel
from accounts.models import User

EMPLOYEE_SALARY, UTILITY_CHARGES, ADVERTISING_MARKETING, RENTAL_FEE = ('hodimlar oyligi', 'komunal tolovlar', 'reklama marketing', 'ijara tolov')

class Payment(BaseModel):
    CATEGORY = (
        (EMPLOYEE_SALARY, EMPLOYEE_SALARY),
        (UTILITY_CHARGES, UTILITY_CHARGES),
        (ADVERTISING_MARKETING, ADVERTISING_MARKETING),
        (RENTAL_FEE, RENTAL_FEE)
    )
    full_name = models.CharField(max_length=250, null=False, blank=False)
    profession = models.CharField(max_length=250, null=True, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=250)

    def __str__(self):
        return f'Tolov - {self.category}'

    @classmethod
    def category_list(cls):
        return [choice[1] for choice in cls.CATEGORY]

    class Meta:
        verbose_name = _('Tolov')
        verbose_name_plural = _('Tolovlar')




