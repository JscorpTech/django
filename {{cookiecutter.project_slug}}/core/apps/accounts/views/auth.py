import uuid
from typing import Type

from core.services import UserService, SmsService
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_core import exceptions
from drf_spectacular.utils import extend_schema
from rest_framework import status, throttling, request
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import GenericViewSet
from django_core.mixins import BaseViewSetMixin
from rest_framework.decorators import action
from ..serializers import (
    RegisterSerializer,
    ConfirmSerializer,
    ResendSerializer,
    ResetPasswordSerializer,
    ResetConfirmationSerializer,
    SetPasswordSerializer,
    UserSerializer,
    UserUpdateSerializer,
)
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password
from drf_spectacular.utils import OpenApiResponse
from rest_framework.permissions import IsAuthenticated
from ..serializers import ChangePasswordSerializer

from .. import models


@extend_schema(tags=["register"])
class RegisterView(BaseViewSetMixin, GenericViewSet, UserService):
    throttle_classes = [throttling.UserRateThrottle]
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        match self.action:
            case "register":
                return RegisterSerializer
            case "confirm":
                return ConfirmSerializer
            case "resend":
                return ResendSerializer
            case _:
                return RegisterSerializer

    @action(methods=["POST"], detail=False, url_path="register")
    def register(self, request):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.data
        phone = data.get("phone")
        # Create pending user
        self.create_user(phone, data.get("first_name"), data.get("last_name"), data.get("password"))
        self.send_confirmation(phone)  # Send confirmation code for sms eskiz.uz
        return Response(
            {"detail": _("Sms %(phone)s raqamiga yuborildi") % {"phone": phone}},
            status=status.HTTP_202_ACCEPTED,
        )

    @extend_schema(summary="Auth confirm.", description="Auth confirm user.")
    @action(methods=["POST"], detail=False, url_path="confirm")
    def confirm(self, request):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.data
        phone, code = data.get("phone"), data.get("code")
        try:
            if SmsService.check_confirm(phone, code=code):
                token = self.validate_user(get_user_model().objects.filter(phone=phone).first())
                return Response(
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

    @action(methods=["POST"], detail=False, url_path="resend")
    def resend(self, rq: Type[request.Request]):
        ser = self.get_serializer(data=rq.data)
        ser.is_valid(raise_exception=True)
        phone = ser.data.get("phone")
        self.send_confirmation(phone)
        return Response({"detail": _("Sms %(phone)s raqamiga yuborildi") % {"phone": phone}})


@extend_schema(tags=["reset-password"])
class ResetPasswordView(BaseViewSetMixin, GenericViewSet, UserService):
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        match self.action:
            case "reset_password":
                return ResetPasswordSerializer
            case "reset_confirm":
                return ResetConfirmationSerializer
            case "reset_password_set":
                return SetPasswordSerializer
            case _:
                return None

    @action(methods=["POST"], detail=False, url_path="reset-password")
    def reset_password(self, request):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        phone = ser.data.get("phone")
        self.send_confirmation(phone)
        return Response({"detail": _("Sms %(phone)s raqamiga yuborildi") % {"phone": phone}})

    @action(methods=["POST"], detail=False, url_path="reset-password-confirm")
    def reset_confirm(self, request):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)

        data = ser.data
        code, phone = data.get("code"), data.get("phone")
        try:
            SmsService.check_confirm(phone, code)
            token = models.ResetToken.objects.create(
                user=get_user_model().objects.filter(phone=phone).first(),
                token=str(uuid.uuid4()),
            )
            return Response(
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

    @action(methods=["POST"], detail=False, url_path="reset-password-set")
    def reset_password_set(self, request):
        ser = self.get_serializer(data=request.data)
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
        return Response({"detail": _("password updated")}, status=status.HTTP_200_OK)


@extend_schema(tags=["me"])
class MeView(BaseViewSetMixin, GenericViewSet, UserService):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        match self.action:
            case "me":
                return UserSerializer
            case "user_update":
                return UserUpdateSerializer
            case _:
                return None

    @action(methods=["GET", "OPTIONS"], detail=False, url_path="me")
    def me(self, request):
        return Response(self.get_serializer(request.user).data)

    @action(methods=["PATCH", "PUT"], detail=False, url_path="user-update")
    def user_update(self, request):
        ser = self.get_serializer(instance=request.user, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response({"detail": _("Malumotlar yangilandi")})


@extend_schema(tags=["change-password"], description="Parolni o'zgartirish uchun")
class ChangePasswordView(BaseViewSetMixin, GenericViewSet):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        request=serializer_class,
        responses={200: OpenApiResponse(ChangePasswordSerializer)},
        summary="Change user password.",
        description="Change password of the authenticated user.",
    )
    @action(methods=["POST"], detail=False, url_path="change-password")
    def change_password(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if user.check_password(request.data["old_password"]):
            user.password = make_password(request.data["new_password"])
            user.save()
            return Response(
                data={"detail": "password changed successfully"},
                status=status.HTTP_200_OK,
            )
        raise PermissionDenied(_("invalida password"))
