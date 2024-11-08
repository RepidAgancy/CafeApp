from django.contrib import admin

from product import models


admin.site.register(models.Product)
admin.site.register(models.CartProduct)
admin.site.register(models.CartItemProduct)
admin.site.register(models.OrderProduct)
admin.site.register(models.CategoryProduct)
