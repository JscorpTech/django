#####################
# Project base django admin register classes
#####################

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin, TabularInline

from core.http.forms import PostAdminForm
from core.http.models import Post, User, SmsConfirm, FrontendTranslation, Comment
from core.http.resources import FrontendTranslationResource
from core.http.resources import PostResource


class PostInline(TabularInline):
    model = Post.comments.through
    fields = ['comment']
    extra = 1


class PostAdmin(TabbedTranslationAdmin, ImportExportModelAdmin, ModelAdmin):
    fields: tuple = ('title', "desc", "image")
    resource_classes: list = [PostResource]
    search_fields: list = ['title', 'desc']
    list_filter = ['title']
    required_languages: tuple = ('uz',)
    form = PostAdminForm
    inlines = [PostInline]


class CustomUserAdmin(UserAdmin, ModelAdmin):
    list_display = ['phone', "first_name", "last_name"]


class FrontendInline(TabularInline):
    model = FrontendTranslation.comments.through
    fields = ['comment']
    extra = 1


class FrontendTranslationAdmin(TabbedTranslationAdmin, ImportExportModelAdmin, ModelAdmin):
    fields: tuple = ("key", "value")
    required_languages: tuple = ('uz',)
    list_display = ["key", "value"]
    inlines = [FrontendInline]

    resource_classes = [FrontendTranslationResource]


class SmsConfirmAdmin(ModelAdmin):
    list_display = ["phone", "code", "resend_count", "try_count"]
    search_fields = ["phone", "code"]


class CommentAdmin(ModelAdmin):
    list_display = ["text"]
    search_fields = ["text"]


admin.site.register(Comment, CommentAdmin)
admin.site.register(FrontendTranslation, FrontendTranslationAdmin)
admin.site.register(SmsConfirm, SmsConfirmAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Post, PostAdmin)
