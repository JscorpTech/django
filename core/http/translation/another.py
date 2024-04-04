#####################
# Django model translation Resources
#####################

from modeltranslation.translator import TranslationOptions




class PostTranslationOption(TranslationOptions):
    fields = ("title", "desc",)


class FrontendTranslationOption(TranslationOptions):
    fields = ("value",)


