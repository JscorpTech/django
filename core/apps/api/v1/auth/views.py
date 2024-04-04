import typing

from django.utils.translation import gettext_lazy as _
from rest_framework import generics, permissions, request, throttling, views

from core import enums, utils, exceptions, services
from core.http import models, serializers, views as http_views


class RegisterView(views.APIView, services.UserService, http_views.ApiResponse):
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
        return self.success(_(enums.Messages.SEND_MESSAGE) % {'phone': phone})


class ConfirmView(views.APIView, services.UserService, http_views.ApiResponse):
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
                return self.success(_(enums.Messages.OTP_CONFIRMED), token=token)
        except exceptions.SmsException as e:
            return utils.ResponseException(e)  # Response exception for APIException
        except Exception as e:
            return self.error(e)  # Api exception for APIException


class ResetPasswordView(http_views.AbstractSendSms):
    """Reset user password"""
    serializer_class: typing.Type[serializers.ResetPasswordSerializer] = serializers.ResetPasswordSerializer


class ResetConfirmationCodeView(views.APIView, http_views.ApiResponse, services.UserService):
    """Reset confirm otp code"""

    serializer_class = serializers.ResetConfirmationSerializer

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
                self.change_password(phone, password)
                return self.success(_(enums.Messages.CHANGED_PASSWORD))
            return self.error(_(enums.Messages.INVALID_OTP))
        except exceptions.SmsException as e:
            return self.error(e, error_code=enums.Codes.INVALID_OTP_ERROR)
        except Exception as e:
            return self.error(e)


class ResendView(http_views.AbstractSendSms):
    """Resend Otp Code"""
    serializer_class = serializers.ResendSerializer


class MeView(views.APIView, http_views.ApiResponse):
    """Get user information"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: request.Request):
        user = request.user
        return self.success(data=serializers.UserSerializer(user).data)
