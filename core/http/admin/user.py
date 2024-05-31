from django.contrib.auth import admin
from unfold.contrib.import_export.admin import ExportActionModelAdmin
from unfold.admin import ModelAdmin
from unfold.forms import (
    UserChangeForm,
    UserCreationForm,
    AdminPasswordChangeForm,
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
