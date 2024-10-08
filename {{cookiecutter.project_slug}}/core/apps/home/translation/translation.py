from modeltranslation import translator
from ..models import FrontendTranslation


class FrontendTranslationOption(translator.TranslationOptions):
    fields = ("value",)


translator.register(FrontendTranslation, FrontendTranslationOption)
