from modeltranslation.translator import translator, TranslationOptions
from common import models


class CategoryModelTranslation(TranslationOptions):
    fields = ('name',)



class FoodModelTranslation(TranslationOptions):
    fields = ('name', 'food_info',)


translator.register(models.CategoryFood, CategoryModelTranslation)
translator.register(models.Food, FoodModelTranslation)