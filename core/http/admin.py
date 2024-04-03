#####################
# Project base django admin register classes
#####################

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.db import models
from django_select2.forms import Select2MultipleWidget
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.import_export.admin import ExportActionModelAdmin

from core.http.forms import PostAdminForm
from core.http.models import Post, User, SmsConfirm, FrontendTranslation, Comment, Tags


class PostInline(TabularInline):
    model = Post.comments.through
    fields = ['comment']
    extra = 1


class TagsInline(TabularInline):
    model = Post.tags.through
    extra = 1


class PostAdmin(TabbedTranslationAdmin, ModelAdmin, ExportActionModelAdmin):
    fields: tuple = ('title', "desc", "image", 'tags')
    search_fields: list = ['title', 'desc']
    list_filter = ['title']
    required_languages: tuple = ('uz',)
    form = PostAdminForm
    inlines = [PostInline]
    formfield_overrides = {
        models.ManyToManyField: {
            "widget": Select2MultipleWidget
        }
    }


class TagsAdmin(ModelAdmin, ExportActionModelAdmin):
    fields: tuple = ('name',)
    search_fields: list = ['name']


class CustomUserAdmin(UserAdmin, ModelAdmin, ExportActionModelAdmin):
    list_display = ['phone', "first_name", "last_name"]


class FrontendInline(TabularInline):
    model = FrontendTranslation.comments.through
    fields = ['comment']
    extra = 1


class FrontendTranslationAdmin(TabbedTranslationAdmin, ModelAdmin, ExportActionModelAdmin):
    fields: tuple = ("key", "value")
    required_languages: tuple = ('uz',)
    list_display = ["key", "value"]
    inlines = [FrontendInline]


class SmsConfirmAdmin(ModelAdmin):
    list_display = ["phone", "code", "resend_count", "try_count"]
    search_fields = ["phone", "code"]


class CommentAdmin(ModelAdmin, ExportActionModelAdmin):
    list_display = ["text"]
    search_fields = ["text"]


class GroupAdmin(ModelAdmin, ExportActionModelAdmin):
    list_display = ['name']
    search_fields = ["name"]
    filter_horizontal = (
        "permissions",
    )


admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)

admin.site.register(Tags, TagsAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(FrontendTranslation, FrontendTranslationAdmin)
admin.site.register(SmsConfirm, SmsConfirmAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Post, PostAdmin)
