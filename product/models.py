from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from common.models import BaseModel

KG, PIECE = ('kg', _('dona'))
APPROVED, NOT_APPROVED  = ('tasdiqlangan', 'tasdiqlanmagan')

class CategoryProduct(BaseModel):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product/category/image/%Y/%m/%d')


class Product(BaseModel):
    category = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=3, default=0.000)
    image = models.ImageField(upload_to='product/product/image/%Y/%m/%d')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('mahsulot')
        verbose_name_plural = _('mahsulotlar')



class CartProduct(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_products')
    total_price = models.DecimalField(max_digits=10, decimal_places=3, default=0.000)
    is_confirm = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.total_price} - umumiy chiqib'

    class Meta:
        verbose_name = _('savatdagi mahsulot')
        verbose_name_plural = _('savatdagi mahsulotlar')


class CartItemProduct(BaseModel):
    UNIT_STATUS = (
        (KG, KG),
        (PIECE, PIECE),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items_products')
    weight = models.PositiveIntegerField(default=0)
    unit_status = models.CharField(max_length=100, choices=UNIT_STATUS)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    cart = models.ForeignKey(CartProduct, on_delete=models.CASCADE, related_name='cart_items_products')

    def __str__(self):
        return f'{self.product.name} - {self.weight} in {self.unit_status}'

    class Meta:
        verbose_name = _('savatdagi mahsulot dona')
        verbose_name_plural = _('savatdagi mahsulotlar dona')


class OrderProduct(BaseModel):
    STATUS = (
        (APPROVED, APPROVED),
        (NOT_APPROVED, NOT_APPROVED),
    )
    cart = models.ForeignKey(CartProduct, on_delete=models.CASCADE, related_name='order_products')
    is_confirm = models.BooleanField(default=False)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.cart} - {self.is_confirm}"

    class Meta:
        verbose_name = _('Buyurtmadagi mahsulot')
        verbose_name_plural = _('Buyurtmadagi mahsulotlar')


