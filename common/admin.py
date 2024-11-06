from django.contrib import admin

from common import models


admin.site.register(models.Table)
admin.site.register(models.Category)
admin.site.register(models.Food)
admin.site.register(models.Cart)
admin.site.register(models.CartItem)
admin.site.register(models.Order)
