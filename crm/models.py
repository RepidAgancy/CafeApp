from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel
from accounts.models import User


class PaymentCategory(BaseModel):
    name = models.CharField(max_length=125)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Tolov usuli')
        verbose_name_plural = _('Tolov usullari')


class Payment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    profession = models.ForeignKey('accounts.Profession', on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    price = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(PaymentCategory, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'Tolov - {self.category.name}'

    class Meta:
        verbose_name = _('Tolov')
        verbose_name_plural = _('Tolovlar')




