"""
Register models
"""
from modeltranslation.translator import translator

from core.http import models
from core.http.translation import another


translator.register(models.Post, another.PostTranslationOption)
translator.register(models.FrontendTranslation, another.FrontendTranslationOption) # noqa
