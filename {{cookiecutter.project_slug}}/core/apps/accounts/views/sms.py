import typing
import uuid
from typing import Type

from core import services
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_core import exceptions
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions
from rest_framework import request
from rest_framework import request as rest_request
from rest_framework import response, status, throttling, views, viewsets
from rest_framework.exceptions import PermissionDenied

from .. import models
from .. import serializers
from .. import serializers as sms_serializers


class AbstractSendSms(views.APIView):
    serializer_class = serializers.ResendSerializer
    throttle_classes = [throttling.UserRateThrottle]
    permission_classes = [permissions.AllowAny]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = services.UserService()

    def post(self, rq: Type[request.Request]):
        ser = self.serializer_class(data=rq.data)
        ser.is_valid(raise_exception=True)
        phone = ser.data.get("phone")
        self.service.send_confirmation(phone)
        return response.Response({"detail": _("Sms %(phone)s raqamiga yuborildi") % {"phone": phone}})


@extend_schema(tags=["register"])
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
        self.create_user(phone, data.get("first_name"), data.get("last_name"), data.get("password"))
        self.send_confirmation(phone)  # Send confirmation code for sms eskiz.uz
        return response.Response(
            {"detail": _("Sms %(phone)s raqamiga yuborildi") % {"phone": phone}},
            status=status.HTTP_202_ACCEPTED,
        )


@extend_schema(tags=["register"])
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
                token = self.validate_user(get_user_model().filter(phone=phone).first())
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


@extend_schema(tags=["reset-password"])
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
                user=get_user_model().filter(phone=phone).first(),
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


@extend_schema(tags=["reset-password"])
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
        return response.Response({"detail": _("password updated")}, status=status.HTTP_200_OK)


@extend_schema(tags=["register"])
class ResendView(AbstractSendSms):
    """Resend Otp Code"""

    serializer_class = serializers.ResendSerializer


@extend_schema(tags=["reset-password"])
class ResetPasswordView(AbstractSendSms):
    """Reset user password"""

    serializer_class: typing.Type[serializers.ResetPasswordSerializer] = serializers.ResetPasswordSerializer


@extend_schema(tags=["me"])
class MeView(viewsets.ViewSet):
    """Get user information"""

    serializer_class = serializers.UserSerializer

    def get(self, request: rest_request.Request):
        user = request.user
        return response.Response(serializers.UserSerializer(user).data)


@extend_schema(tags=["me"])
class MeUpdateView(generics.UpdateAPIView):
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user
