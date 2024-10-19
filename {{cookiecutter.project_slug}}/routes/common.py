"""
All urls configurations tree
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve


urlpatterns = [
    path("admin/", admin.site.urls),
    path("rosetta/", include("rosetta.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
    path("", include("core.apps.accounts.urls")),
    path(
        "ckeditor5/",
        include("django_ckeditor_5.urls"),
        name="ck_editor_5_upload_file",
    ),
    re_path(
        r"static/(?P<path>.*)", serve, {"document_root": settings.STATIC_ROOT}
    ),
    re_path(
        r"media/(?P<path>.*)", serve, {"document_root": settings.MEDIA_ROOT}
    ),
]