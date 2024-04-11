from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from django.views.static import serve

from routes.swagger import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path("rosetta/", include("rosetta.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
    path("i18n/", include("django.conf.urls.i18n")),

    #####################
    # My apps
    #####################
    path("api/", include("core.apps.accounts.urls")),
    path('', include('core.apps.home.urls')),

    #####################
    # Media and static files
    #####################
    re_path(r"static/(?P<path>.*)", serve, {"document_root": settings.STATIC_ROOT}),
    re_path(r"media/(?P<path>.*)", serve, {"document_root": settings.MEDIA_ROOT}),

    #####################
    # Swagger urls
    #####################
    path('swagger<format>/', schema_view.without_ui(cache_timeout=120), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=120), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=120), name='schema-redoc'),
]
