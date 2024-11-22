import typing
import uuid

from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework import request as rest_request
from rest_framework import response, status, throttling, views, viewsets

from core import services
from core.apps.accounts import models
from core.apps.accounts import serializers as sms_serializers
from core.http import serializers, exceptions
from core.http import views as http_views
from core.http.models import User


class RegisterView(views.APIView, services.UserService):
    """Register new user"""

    serializer_class = serializers.RegisterSerializer
    throttle_classes = [throttling.UserRateThrottle]
    permission_classes = [permissions.AllowAny]

    def post(self, request: rest_request.Request):
        ser = self.serializer_class(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.data
        phone = data.get("phone")
        # Create pending user
        self.create_user(
            phone,
            data.get("first_name"),
            data.get("last_name"),
            data.get("password"),
        )
        self.send_confirmation(phone)  # Send confirmation code for sms eskiz.uz
        return response.Response(
            {"detail": _("Sms %(phone)s raqamiga yuborildi") % {"phone": phone}},
            status=status.HTTP_202_ACCEPTED,
        )


class ConfirmView(views.APIView, services.UserService):
    """Confirm otp code"""

    serializer_class = serializers.ConfirmSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=serializer_class,
        summary="Auth confirm.",
        description="Auth confirm user.",
    )
    def post(self, request: rest_request.Request):
        ser = self.serializer_class(data=request.data)
        ser.is_valid(raise_exception=True)

        data = ser.data
        phone, code = data.get("phone"), data.get("code")

        try:
            # Check Sms confirmation otp code
            if services.SmsService.check_confirm(phone, code=code):
                # Create user
                token = self.validate_user(User.objects.filter(phone=phone).first())
                return response.Response(
                    data={
                        "detail": _("Tasdiqlash ko'di qabul qilindi"),
                        "token": token,
                    },
                    status=status.HTTP_202_ACCEPTED,
                )
        except exceptions.SmsException as e:
            raise PermissionDenied(e)  # Response exception for APIException
        except Exception as e:
            raise PermissionDenied(e)  # Api exception for APIException


class ResetConfirmationCodeView(views.APIView, services.UserService):
    """Reset confirm otp code"""

    serializer_class = serializers.ResetConfirmationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request: rest_request.Request):
        ser = self.serializer_class(data=request.data)
        ser.is_valid(raise_exception=True)

        data = ser.data
        code, phone = data.get("code"), data.get("phone")
        try:
            services.SmsService.check_confirm(phone, code)
            token = models.ResetToken.objects.create(
                user=User.objects.filter(phone=phone).first(),
                token=str(uuid.uuid4()),
            )
            return response.Response(
                data={
                    "token": token.token,
                    "created_at": token.created_at,
                    "updated_at": token.updated_at,
                },
                status=status.HTTP_200_OK,
            )
        except exceptions.SmsException as e:
            raise PermissionDenied(str(e))
        except Exception as e:
            raise PermissionDenied(str(e))


class ResetSetPasswordView(views.APIView, services.UserService):
    serializer_class = sms_serializers.SetPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        ser = self.serializer_class(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.data
        token = data.get("token")
        password = data.get("password")
        token = models.ResetToken.objects.filter(token=token)
        if not token.exists():
            raise PermissionDenied(_("Invalid token"))
        phone = token.first().user.phone
        token.delete()
        self.change_password(phone, password)
        return response.Response(
            {"detail": _("password updated")}, status=status.HTTP_200_OK
        )


class ResendView(http_views.AbstractSendSms):
    """Resend Otp Code"""

    serializer_class = serializers.ResendSerializer


class ResetPasswordView(http_views.AbstractSendSms):
    """Reset user password"""

    serializer_class: typing.Type[serializers.ResetPasswordSerializer] = (
        serializers.ResetPasswordSerializer
    )


class MeView(viewsets.ViewSet):
    """Get user information"""

    serializer_class = serializers.UserSerializer

    def get(self, request: rest_request.Request):
        user = request.user
        return response.Response(serializers.UserSerializer(user).data)


class MeUpdateView(generics.UpdateAPIView):
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user
