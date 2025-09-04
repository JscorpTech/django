"""
All urls configurations tree
"""

from config.env import env
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path, re_path
from django.views.static import serve
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)


def home(request):
    return HttpResponse("OK")

################
# My apps url
################
urlpatterns = [
    path("health/", home),
    path("", include("core.apps.accounts.urls")),
]


################
# Library urls
################
urlpatterns += [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
    {% if cookiecutter.rosetta %}path("rosetta/", include("rosetta.urls")),{% endif %}
    {% if cookiecutter.ckeditor %}path("ckeditor5/", include("django_ckeditor_5.urls"), name="ck_editor_5_upload_file"),{% endif %}
]

################
# Project env debug mode
################
if env.str("PROJECT_ENV") == "debug":
    urlpatterns += [
        {% if cookiecutter.silk %}path('silk/', include('silk.urls', namespace='silk')){% endif %}
    ]

    ################
    # Swagger urls
    ################
    urlpatterns += [
        path("schema/", SpectacularAPIView.as_view(), name="schema"),
        path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
        path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    ]

################
# Media urls
################
urlpatterns += [
    re_path(r"static/(?P<path>.*)", serve, {"document_root": settings.STATIC_ROOT}),
    re_path(r"media/(?P<path>.*)", serve, {"document_root": settings.MEDIA_ROOT}),
]
