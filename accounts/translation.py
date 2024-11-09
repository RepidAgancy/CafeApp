from modeltranslation.translator import TranslationOptions
from modeltranslation import translator

from accounts import models


@translator.register(models.Profession)
class ProfessionTranslationOptions(TranslationOptions):
    fields = ('name',)
