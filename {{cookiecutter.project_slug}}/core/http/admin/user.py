from unfold.admin import ModelAdmin
from django.contrib.auth import admin
from django.utils.translation import gettext_lazy as _
from unfold.forms import (
    AdminPasswordChangeForm,
    UserChangeForm,
    # UserCreationForm,
)


class CustomUserAdmin(admin.UserAdmin, ModelAdmin):
    change_password_form = AdminPasswordChangeForm
    # add_form = UserCreationForm
    form = UserChangeForm
    list_display = (
        "first_name",
        "last_name",
        "phone",
    )
    fieldsets = ((None, {"fields": ("phone",)}),) + (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )


class GroupAdmin(ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    filter_horizontal = ("permissions",)


class SmsConfirmAdmin(ModelAdmin):
    list_display = ["phone", "code", "resend_count", "try_count"]
    search_fields = ["phone", "code"]
