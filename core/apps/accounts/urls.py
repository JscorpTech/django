from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from core.apps.accounts import views

urlpatterns = [
    path('auth/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login view
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token view
    path('auth/token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),  # Verify token
    path("auth/register/", views.RegisterView.as_view(), name="register"),  # Register
    path("auth/confirm/", views.ConfirmView.as_view(), name="confirm"),  # Confirm Otp code view
    path("auth/reset/password/", views.ResetPasswordView.as_view(), name="reset-password"),  # Reset password step 1
    path("auth/confirm/reset/", views.ResetConfirmationCodeView.as_view(), name="reset-confirmation-code"),
    # Reset password step 2
    path("auth/resend/", views.ResendView.as_view(), name="resend"),  # resend otp code
    path("auth/me/", views.MeView.as_view(), name="me"),  # get user information
]
