from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline
from core.apps.shared.models import SettingsModel, OptionsModel


class OptionsInline(StackedInline):
    model = OptionsModel
    extra = 1


@admin.register(SettingsModel)
class SettingsAdmin(ModelAdmin):
    list_display = ["id", "key"]
    inlines = [OptionsInline]
