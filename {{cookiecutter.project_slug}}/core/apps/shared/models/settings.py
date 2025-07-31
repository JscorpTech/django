from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel


class SettingsModel(AbstractBaseModel):
    key = models.CharField(_("key"))
    is_public = models.BooleanField(_("is public"), default=False)
    description = models.TextField(_("description"), blank=True, null=True)

    class Meta:
        db_table = "settings"
        verbose_name = _("Settings")
        verbose_name_plural = _("Settings")


class OptionsModel(models.Model):
    settings = models.ForeignKey(
        "SettingsModel", verbose_name=_("settings"), on_delete=models.CASCADE, related_name="options"
    )
    key = models.CharField(_("key"), max_length=255)
    value = ArrayField(
        models.CharField(_("value"), max_length=255),
        verbose_name=_("value"),
    )

    class Meta:
        db_table = "options"
        verbose_name = _("Options")
        verbose_name_plural = _("Options")
