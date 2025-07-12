from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline
from core.apps.shared.models import SettingsModel, OptionsModel
from unfold.contrib.forms.widgets import ArrayWidget
from django.contrib.postgres.fields import ArrayField


class OptionsInline(StackedInline):
    model = OptionsModel
    extra = 1
    formfield_overrides = {
        ArrayField: {"widget": ArrayWidget},
    }


@admin.register(SettingsModel)
class SettingsAdmin(ModelAdmin):
    list_display = ["id", "key"]
    inlines = [OptionsInline]

