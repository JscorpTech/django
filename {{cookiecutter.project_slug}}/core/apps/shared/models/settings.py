from django.db import models
from django.utils.translation import gettext_lazy as _


class SettingsModel(models.Model):
    key = models.CharField(_("key"))

    class Meta:
        db_table = "settings"
        verbose_name = _("Settings")
        verbose_name_plural = _("Settings")


class OptionsModel(models.Model):
    settings = models.ForeignKey(
        "SettingsModel", verbose_name=_("settings"), on_delete=models.CASCADE, related_name="options"
    )
    key = models.CharField(_("key"))
    value = models.CharField(_("value"))

    class Meta:
        db_table = "options"
        verbose_name = _("Options")
        verbose_name_plural = _("Options")
