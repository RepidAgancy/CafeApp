from django.db import models
from django.utils.translation import gettext_lazy as _


BUSY, NOT_BUSY = (_('band'), _('band emas'))
IN_PROCESS, DONE = (_('jarayonda'), _('bajarildi'))
PROFIT, EXPENSE = (_('kirim'), _('chiqim'))

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Table(BaseModel):
    TYPE = (
        (BUSY, BUSY),
        (NOT_BUSY, NOT_BUSY),
    )
    number = models.PositiveIntegerField(unique=True, default=0)
    type = models.CharField(max_length=20, choices=TYPE, default=NOT_BUSY)

    def __str__(self):
        return f'{self.number} - stol'

    class Meta:
        verbose_name = _('stol')
        verbose_name_plural = _('stollar')


class CategoryFood(BaseModel):
    image = models.ImageField(upload_to='common/category/image/%Y/%m/%d')
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('kategoriya')
        verbose_name_plural = _('kategoriylar')


class Food(BaseModel):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='common/food/image/%Y/%m/%d')
    price = models.PositiveIntegerField()
    category = models.ForeignKey(CategoryFood, on_delete=models.CASCADE, related_name='food')
    food_info = models.TextField()
    food_composition = models.TextField()

    def __str__(self):
        return f'{self.name} - {self.price} UZS'

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
    type = models.CharField(max_length=20, choices=TYPE)

    def __str__(self):
        return f'{self.cart} - {self.status}'



