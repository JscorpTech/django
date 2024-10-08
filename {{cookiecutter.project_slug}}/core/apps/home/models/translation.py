from django.db import models
from django.utils.translation import gettext as _
from core.http.models import AbstractBaseModel


class FrontendTranslation(AbstractBaseModel):
    key = models.CharField(max_length=255, unique=True)
    value = models.TextField()

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = _("Frontend Translation")
        verbose_name_plural = _("Frontend Translations")
