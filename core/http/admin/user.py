from django.contrib.auth import admin
from unfold.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from unfold.forms import (
    AdminPasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
)


class CustomUserAdmin(admin.UserAdmin, ModelAdmin):
    change_password_form = AdminPasswordChangeForm
    add_form = UserCreationForm
    form = UserChangeForm
    list_display = (
        "first_name",
        "last_name",
        "phone",
    )
    fieldsets = ((None, {"fields": ("phone",)}),) + UserAdmin.fieldsets


class GroupAdmin(ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    filter_horizontal = ("permissions",)
