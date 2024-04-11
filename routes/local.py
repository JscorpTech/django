from django.urls import path, include

urlpatterns = [
    path("debug", include("debug_toolbar.urls")),
]
