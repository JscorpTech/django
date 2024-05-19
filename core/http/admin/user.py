from django.contrib.auth import admin
from import_export import admin as import_export


class CustomUserAdmin(admin.UserAdmin, import_export.ImportExportModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "phone",
    )


class GroupAdmin(import_export.ImportExportModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    filter_horizontal = ("permissions",)
