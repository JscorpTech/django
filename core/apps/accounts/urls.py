"""
Accounts app urls
"""

from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from core.apps.accounts import views

urlpatterns = [
    path("auth/confirm/", views.ConfirmView.as_view(), name="confirm"),
    path("auth/register/", views.RegisterView.as_view(), name="register"),
    path("auth/resend/", views.ResendView.as_view(), name="resend"),
    path("auth/me/", views.MeView.as_view({"get": "get"}), name="me"),
    path("auth/me/update/", views.MeUpdateView.as_view(), name="me-update"),
    path(
        "auth/token/",
        jwt_views.TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "auth/token/refresh/",
        jwt_views.TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "auth/token/verify/",
        jwt_views.TokenVerifyView.as_view(),
        name="token_verify",
    ),
    path(
        "auth/reset/password/",
        views.ResetPasswordView.as_view(),
        name="reset-password",
    ),
    path(
        "auth/reset/confirm/",
        views.ResetConfirmationCodeView.as_view(),
        name="reset-confirmation-code",
    ),
    path(
        "auth/reset/set/",
        views.ResetSetPasswordView.as_view(),
        name="set-password",
    ),
    path(
        "auth/change/password/",
        views.ChangePasswordView.as_view(),
        name="change-password",
    ),
]
