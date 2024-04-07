from datetime import datetime
from typing import Union

from django.contrib.auth import hashers
from rest_framework_simplejwt.tokens import RefreshToken

from core.exceptions import SmsException
from core.http.models import User
from core.services.base_service import BaseService
from core.services.sms import SmsService
from core.utils.exception import ResponseException


class UserService(BaseService, SmsService):

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def create_user(self, phone, first_name, last_name, password):
        User.objects.update_or_create(phone=phone, defaults={
            "phone": phone, "first_name": first_name,
            "last_name": last_name, "password": hashers.make_password(password),
        })

    def send_confirmation(self, phone) -> bool:
        try:
            self.send_confirm(phone)
            return True
        except SmsException as e:
            ResponseException(e, data={"expired": e.kwargs.get("expired")})
        except Exception as e:
            ResponseException(e)

    def validate_user(self, user: Union[User]) -> dict:
        """Create user if user not found"""

        user.validated_at = datetime.now()
        user.save()
        token = self.get_token(user)
        return token

    def is_validated(self, user: Union[User]) -> bool:
        """User is validated check"""

        if user.validated_at is not None:
            return True
        return False

    def change_password(self, phone, password):
        """Change password"""

        user = User.objects.filter(phone=phone).first()
        user.set_password(password)
        user.save()
