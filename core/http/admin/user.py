from django.contrib.auth import admin
from unfold.admin import ModelAdmin
from unfold.contrib.import_export.admin import ExportActionModelAdmin
from unfold.forms import (
    AdminPasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
)


class CustomUserAdmin(admin.UserAdmin, ExportActionModelAdmin, ModelAdmin):
    change_password_form = AdminPasswordChangeForm
    add_form = UserCreationForm
    form = UserChangeForm
    list_display = (
        "first_name",
        "last_name",
        "phone",
    )


class GroupAdmin(ExportActionModelAdmin, ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    filter_horizontal = ("permissions",)
