from modeltranslation import translator
from ..models import Post


class PostTranslationOption(translator.TranslationOptions):
    fields = (
        "title",
        "desc",
    )


translator.register(Post, PostTranslationOption)