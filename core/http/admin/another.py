from django.db import models as db_model
from django_select2 import forms as django_select2
from modeltranslation import admin as modeltranslation
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.import_export.admin import ExportActionModelAdmin

from core.http import forms, models


class PostInline(TabularInline):
    model = models.Post.comments.through
    fields = ["comment"]
    extra = 1


class TagsInline(TabularInline):
    model = models.Post.tags.through
    extra = 1


class PostAdmin(
    modeltranslation.TabbedTranslationAdmin,
    ExportActionModelAdmin,
    ModelAdmin,
):  # noqa
    fields: tuple = ("title", "desc", "image", "tags")
    search_fields: list = ["title", "desc"]
    list_filter = ["title"]
    required_languages: tuple = ("uz",)
    form = forms.PostAdminForm
    inlines = [PostInline]
    formfield_overrides = {
        db_model.ManyToManyField: {
            "widget": django_select2.Select2MultipleWidget
        }
    }


class TagsAdmin(ExportActionModelAdmin, ModelAdmin):
    fields: tuple = ("name",)
    search_fields: list = ["name"]


class FrontendTranslationAdmin(ModelAdmin, ExportActionModelAdmin):  # noqa
    fields: tuple = ("key", "value")
    required_languages: tuple = ("uz",)
    list_display = ["key", "value"]


class SmsConfirmAdmin(ModelAdmin):
    list_display = ["phone", "code", "resend_count", "try_count"]
    search_fields = ["phone", "code"]


class CommentAdmin(ExportActionModelAdmin, ModelAdmin):
    list_display = ["text"]
    search_fields = ["text"]
