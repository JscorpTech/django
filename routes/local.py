"""
Local urls for debugging
"""

from django.urls import path
from django.urls import include

urlpatterns = [
    path("debug", include("debug_toolbar.urls")),
]
