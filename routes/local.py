"""
Local urls for debugging
"""

from django.urls import include, path

urlpatterns = [
    path("debug", include("debug_toolbar.urls")),
]
