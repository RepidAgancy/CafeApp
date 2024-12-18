from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from common.models import BaseModel, EXPENSE, PROFIT

KG, PIECE = ('kg', _('dona'))
APPROVED, NOT_APPROVED = ('tasdiqlangan', 'tasdiqlanmagan')


class CategoryProduct(BaseModel):
    name_uz = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product/category/')

    def __str__(self):
        return self.name_uz


class Product(BaseModel):
    category = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, related_name='products')
    name_uz = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product/product/')

    def save(self, *args, **kwargs):
        if self.image:
            image = Image.open(self.image)
            image = image.convert("RGB")

            max_size = (1024, 1024)
            image.thumbnail(max_size, Image.Resampling.LANCZOS)

            buffer = BytesIO()
            image.save(buffer, format='WEBP', quality=80, optimize=True)
            buffer.seek(0)

            new_image_name = f"{self.image.name.split('.')[0]}.webp"
            self.image.save(
                new_image_name,
                ContentFile(buffer.read()),
                save=False
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name_uz

    class Meta:
        verbose_name = _('mahsulot')
        verbose_name_plural = _('mahsulotlar')


class CartProduct(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_products')
    total_price = models.PositiveIntegerField(default=0)
    is_confirm = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.total_price} - umumiy chiqim'

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
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.product.name_uz} - {self.weight} in {self.unit_status}'

    class Meta:
        verbose_name = _('savatdagi mahsulot dona')
        verbose_name_plural = _('savatdagi mahsulotlar dona')

    @classmethod
    def get_unit_status(cls):
        return[choice[1] for choice in cls.UNIT_STATUS]


class OrderProduct(BaseModel):
    STATUS = (
        (APPROVED, APPROVED),
        (NOT_APPROVED, NOT_APPROVED),
    )
    TYPE = (
        (PROFIT, PROFIT),
        (EXPENSE, EXPENSE),
    )
    cart = models.ForeignKey(CartProduct, on_delete=models.CASCADE, related_name='order_products')
    is_confirm = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=STATUS)
    type = models.CharField(max_length=250, choices=TYPE, default=EXPENSE)

    def __str__(self):
        return f"{self.cart} - {self.is_confirm}"

    class Meta:
        verbose_name = _('Buyurtmadagi mahsulot')
        verbose_name_plural = _('Buyurtmadagi mahsulotlar')


