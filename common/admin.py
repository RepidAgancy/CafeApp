from django.contrib import admin
from django.utils.html import format_html

from common import models

@admin.register(models.Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'is_busy')
    list_editable = ['is_busy']

    def is_busy(self, obj):
        return format_html('<input type="checkbox" {} disabled>', 'checked' if obj.is_busy else '')
    is_busy.short_description = 'Checked Status'


admin.site.register(models.CategoryFood)
admin.site.register(models.Food)
admin.site.register(models.Cart)
admin.site.register(models.CartItem)
admin.site.register(models.Order)
