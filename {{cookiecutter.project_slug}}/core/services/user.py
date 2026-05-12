import uuid

from django.contrib.auth import get_user_model, hashers
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext as _
from django_core import exceptions
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt import tokens

from core.apps.accounts import models
from core.services import sms


class UserService(sms.SmsService):
    def get_token(self, user):
        refresh = tokens.RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    @transaction.atomic
    def create_user(self, phone, first_name, last_name, password):
        user, _created = get_user_model().objects.update_or_create(
            phone=phone,
            defaults={
                "phone": phone,
                "first_name": first_name,
                "last_name": last_name,
                "password": hashers.make_password(password),
            },
        )
        return user

    def send_confirmation(self, phone) -> bool:
        try:
            self.send_confirm(phone)
            return True
        except exceptions.SmsException as e:
            raise PermissionDenied(_("Qayta sms yuborish uchun kuting: {}").format(e.kwargs.get("expired")))
        except Exception:
            raise PermissionDenied(_("Serverda xatolik yuz berdi"))

    @transaction.atomic
    def validate_user(self, user) -> dict:
        if user is None:
            raise PermissionDenied(_("User does not exist"))

        if user.validated_at is None:
            user.validated_at = timezone.now()
            user.save(update_fields=["validated_at", "updated_at"])

        return self.get_token(user)

    def confirm_user(self, phone, code) -> dict:
        try:
            sms.SmsService.check_confirm(phone, code=code)
        except exceptions.SmsException as exc:
            raise PermissionDenied(str(exc))

        user = get_user_model().objects.filter(phone=phone).first()
        return self.validate_user(user)

    @transaction.atomic
    def create_reset_token(self, phone, code) -> models.ResetToken:
        try:
            sms.SmsService.check_confirm(phone, code=code)
        except exceptions.SmsException as exc:
            raise PermissionDenied(str(exc))

        user = get_user_model().objects.filter(phone=phone).first()
        if user is None:
            raise PermissionDenied(_("User does not exist"))

        return models.ResetToken.objects.create(user=user, token=str(uuid.uuid4()))

    def is_validated(self, user) -> bool:
        """
        User is validated check
        """
        if user.validated_at is not None:
            return True
        return False

    @transaction.atomic
    def set_password_with_reset_token(self, token, password):
        reset_token = models.ResetToken.objects.select_related("user").filter(token=token).first()
        if reset_token is None:
            raise PermissionDenied(_("Invalid token"))

        user = reset_token.user
        reset_token.delete()
        user.set_password(password)
        user.save(update_fields=["password", "updated_at"])
        return user

    @transaction.atomic
    def change_password(self, phone, password):
        user = get_user_model().objects.filter(phone=phone).first()
        if user is None:
            raise PermissionDenied(_("User does not exist"))
        user.set_password(password)
        user.save(update_fields=["password", "updated_at"])
        return user

    @transaction.atomic
    def change_authenticated_password(self, user, old_password, new_password):
        if not user.check_password(old_password):
            raise PermissionDenied(_("Invalid password"))

        user.set_password(new_password)
        user.save(update_fields=["password", "updated_at"])
        return user
