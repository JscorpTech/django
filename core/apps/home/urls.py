"""
Home app urls
"""

from django.urls import path
from django.urls import include

from rest_framework import routers

from core.apps.home import views

router = routers.DefaultRouter()
router.register("", views.PostListView, basename="posts")

urlpatterns = [
    path(
        "messages/",
        views.FrontendTranslationView.as_view(),
        name="frontend-translation",
    ),  # noqa
    path("posts/", include(router.urls), name="posts"),
    path("", views.HomeView.as_view(), name="home"),
]
