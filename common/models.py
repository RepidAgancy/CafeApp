from django.db import models

from accounts.models import User

BUSY, NOT_BUSY = ('band', 'band emas')
FOOD, PRODUCT = ('food', 'product')
IN_PROCESS, DONE = ('jarayonda', 'bajarildi')

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
    number = models.IntegerField(unique=True, default=0)
    type = models.CharField(max_length=20, choices=TYPE, default=NOT_BUSY)

    def __str__(self):
        return f'{self.number} - stol'


class Category(BaseModel):
    TYPE = (
        (FOOD, FOOD),
        (PRODUCT, PRODUCT),
    )
    image = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20, choices=TYPE)

    def __str__(self):
        return f'{self.name} - {self.type}'


class Food(BaseModel):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/')
    price = models.DecimalField(max_digits=10, decimal_places=3)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    food_info = models.TextField()
    food_composition = models.TextField()

    def __str__(self):
        return f'{self.name} - {self.price} UZS'


class Cart(BaseModel):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=3, default=0.000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return f'{self.table} - {self.total_price}'


class CartItem(BaseModel):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return f'{self.food} - {self.quantity}'


class Order(BaseModel):
    STATUS = (
        (IN_PROCESS, IN_PROCESS),
        (DONE, DONE),
    )
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS, default=IN_PROCESS)
    is_confirm = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.cart} - {self.status}'

