import typing
from datetime import datetime

from django.contrib.auth import hashers
from rest_framework_simplejwt import tokens


from core import exceptions
from core.http import models
from core.utils import exception

from core.services import sms
from core.services import base_service


class UserService(base_service.BaseService, sms.SmsService):

    def get_token(self, user):
        refresh = tokens.RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def create_user(self, phone, first_name, last_name, password):
        models.User.objects.update_or_create(phone=phone, defaults={
            "phone": phone,
            "first_name": first_name,
            "last_name": last_name,
            "password": hashers.make_password(password)
        })

    def send_confirmation(self, phone) -> bool:
        try:
            self.send_confirm(phone)
            return True
        except exceptions.SmsException as e:
            exception.ResponseException(e, data={"expired": e.kwargs.get("expired")}) # noqa
        except Exception as e:
            exception.ResponseException(e)

    def validate_user(self, user: typing.Union[models.User]) -> dict:
        """
        Create user if user not found
        """
        user.validated_at = datetime.now()
        user.save()
        token = self.get_token(user)
        return token

    def is_validated(self, user: typing.Union[models.User]) -> bool:
        """
        User is validated check
        """
        if user.validated_at is not None:
            return True
        return False

    def change_password(self, phone, password):
        """
        Change password
        """
        user = models.User.objects.filter(phone=phone).first()
        user.set_password(password)
        user.save()
