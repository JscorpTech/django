"""
Django model translation resources
"""

from modeltranslation import translator


class PostTranslationOption(translator.TranslationOptions):
    fields = (
        "title",
        "desc",
    )


class FrontendTranslationOption(translator.TranslationOptions):
    fields = ("value",)
