#####################
# Register models
#####################

from modeltranslation.translator import translator

from core.http.models import Post, FrontendTranslation
from . import another

translator.register(Post, another.PostTranslationOption)
translator.register(FrontendTranslation, another.FrontendTranslationOption)
