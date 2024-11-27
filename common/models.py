from io import BytesIO

from PIL import Image
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.files.base import ContentFile


IN_PROCESS, DONE = (_('jarayonda'), _('bajarildi'))
PROFIT, EXPENSE = (_('kirim'), _('chiqim'))


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Table(BaseModel):
    number = models.PositiveIntegerField(unique=True, default=0)
    is_busy = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.number} - stol'

    class Meta:
        verbose_name = _('stol')
        verbose_name_plural = _('stollar')


class CategoryFood(BaseModel):
    image = models.ImageField(upload_to='common/category/')
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('kategoriya taom')
        verbose_name_plural = _('kategoriylar taom')


class Food(BaseModel):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='common/food/')
    price = models.PositiveIntegerField()
    category = models.ForeignKey(CategoryFood, on_delete=models.CASCADE, related_name='food')
    food_info = models.TextField()

    def __str__(self):
        return f'{self.name} - {self.price} UZS'

    def save(self, *args, **kwargs):
        if self.image:
            # Faylni o'qish
            image = Image.open(self.image)
            image = image.convert("RGB")  # RGB formatga o'tkazish (WebP faqat RGB-ni qo'llab-quvvatlaydi)

            # Rasmning maksimal o'lchamini belgilash (masalan, 1024x1024)
            max_size = (1024, 1024)  # Rasmning maksimal o'lchamini 1024x1024 px qilish
            image.thumbnail(max_size, Image.Resampling.LANCZOS)

            # Faylni WebP formatida saqlash (sifatni kamaytirish)
            buffer = BytesIO()
            image.save(buffer, format='WEBP', quality=80, optimize=True)  # 80% sifatda saqlash
            buffer.seek(0)  # Faylni boshidan o'qish

            # Yangi WebP formatidagi faylni saqlash
            new_image_name = f"{self.image.name.split('.')[0]}.webp"  # Yangi nom (webp formatida)
            self.image.save(
                new_image_name,
                ContentFile(buffer.read()),  # Yangi faylni saqlash
                save=False  # Django avtomatik saqlashni oldini olish
            )

        # Super metodni chaqirish
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('toam')
        verbose_name_plural = _('toamlar')


class Cart(BaseModel):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    total_price = models.PositiveIntegerField(default=0.000)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='orders')
    is_confirm = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.table} - {self.total_price}'

    class Meta:
        verbose_name = _("savat")
        verbose_name_plural = _("savatlar")


class CartItem(BaseModel):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return f'{self.food} - {self.quantity}'

    class Meta:
        verbose_name = _("savatdagi taom")
        verbose_name_plural = _("savatdagi taomlar")


class Order(BaseModel):
    STATUS = (
        (IN_PROCESS, IN_PROCESS),
        (DONE, DONE),
    )
    TYPE = (
        (PROFIT, PROFIT),
        (EXPENSE, EXPENSE),
    )
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS, default=IN_PROCESS)
    is_confirm = models.BooleanField(default=False)
    type = models.CharField(max_length=20, choices=TYPE, default=PROFIT)


    def __str__(self):
        return f'{self.cart} - {self.status}'



