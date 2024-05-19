from django.contrib import admin
from django.db import models as db_model
from import_export import admin as import_export
from django_select2 import forms as django_select2
from modeltranslation import admin as modeltranslation

from core.http import forms
from core.http import models


class PostInline(admin.TabularInline):
    model = models.Post.comments.through
    fields = ["comment"]
    extra = 1


class TagsInline(admin.TabularInline):
    model = models.Post.tags.through
    extra = 1


class PostAdmin(
    modeltranslation.TabbedTranslationAdmin,
    import_export.ImportExportModelAdmin,
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


class TagsAdmin(import_export.ImportExportModelAdmin):
    fields: tuple = ("name",)
    search_fields: list = ["name"]


class FrontendTranslationAdmin(import_export.ImportExportModelAdmin):  # noqa
    fields: tuple = ("key", "value")
    required_languages: tuple = ("uz",)
    list_display = ["key", "value"]


class SmsConfirmAdmin(admin.ModelAdmin):
    list_display = ["phone", "code", "resend_count", "try_count"]
    search_fields = ["phone", "code"]


class CommentAdmin(import_export.ImportExportModelAdmin):
    list_display = ["text"]
    search_fields = ["text"]
