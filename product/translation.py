from modeltranslation.translator import TranslationOptions, register

from product import models

@register(models.Product)
class ProductModelTranslation(TranslationOptions):
    fields = ('name', )

@register(models.CategoryProduct)
class ProductCategoryModelTranslation(TranslationOptions):
    fields = ('name', )


