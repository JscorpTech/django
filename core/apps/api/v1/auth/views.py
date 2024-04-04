import typing

from django.utils.translation import gettext_lazy as _
from rest_framework import generics, permissions, request, throttling, views

from core import enums, utils, exceptions, services
from core.http import models, serializers
from core.http import views as http_views


class RegisterView(views.APIView, services.UserService):
    """Register new user"""

    serializer_class = serializers.RegisterSerializer
    throttle_classes = [throttling.UserRateThrottle]

    def post(self, request: request.Request):
        ser = self.serializer_class(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.data
        phone = data.get("phone")

        # Create pending user
        self.create_pending_user(
            phone, data.get("first_name"),
            data.get("last_name"), data.get("password")
        )

        self.send_confirmation(phone)  # Send confirmation code for sms eskiz.uz
        return utils.ApiResponse().success(_(enums.Messages.SEND_MESSAGE) % {'phone': phone})


class ConfirmView(views.APIView, services.UserService):
    """Confirm otp code"""

    serializer_class = serializers.ConfirmSerializer

    def post(self, request: request.Request):
        ser = self.serializer_class(data=request.data)
        ser.is_valid(raise_exception=True)

        data = ser.data
        phone = data.get("phone")
        code = data.get("code")

        try:
            pending_user = generics.get_object_or_404(models.PendingUser, phone=phone)

            # Check Sms confirmation otp code
            if services.SmsService.check_confirm(phone, code=code):
                # Create user
                token = self.create_user_from_pending(pending_user)
                return utils.ApiResponse().success(_(enums.Messages.OTP_CONFIRMED), token=token)
        except exceptions.SmsException as e:
            return utils.ResponseException(e)  # Response exception for APIException
        except Exception as e:
            return utils.ApiResponse().error(e)  # Api exception for APIException


class ResetPasswordView(http_views.AbstractSendSms):
    """Reset user password"""
    serializer_class: typing.Type[serializers.ResetPasswordSerializer] = serializers.ResetPasswordSerializer


class ResetConfirmationCodeView(views.APIView):
    """Reset confirm otp code"""

    serializer_class = serializers.ResetConfirmationSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = services.UserService()

    def post(self, request: request.Request):
        ser = self.serializer_class(data=request.data)
        ser.is_valid(raise_exception=True)

        data = ser.data
        code = data.get('code')
        phone = data.get('phone')
        password = data.get('password')

        try:
            res = services.SmsService.check_confirm(phone, code)
            if res:
                self.service.change_password(phone, password)
                return utils.ApiResponse().success(_(enums.Messages.CHANGED_PASSWORD))
            return utils.ApiResponse().error(_(enums.Messages.INVALID_OTP))
        except exceptions.SmsException as e:
            return utils.ApiResponse().error(e, error_code=enums.Codes.INVALID_OTP_ERROR)
        except Exception as e:
            return utils.ApiResponse().error(e)


class ResendView(http_views.AbstractSendSms):
    """Resend Otp Code"""
    serializer_class = serializers.ResendSerializer


class MeView(views.APIView):
    """Get user information"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: request.Request):
        user = request.user
        return utils.ApiResponse().success(data=serializers.UserSerializer(user).data)
