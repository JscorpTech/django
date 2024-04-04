from django.utils.translation import gettext as _
from rest_framework_simplejwt.tokens import RefreshToken

from core.enums import Messages, Codes
from core.exceptions import SmsException
from core.http.models import PendingUser, User
from core.services.base_service import BaseService
from core.services.sms import SmsService
from core.utils.exception import ResponseException


class UserService(BaseService, SmsService):

    def get_token(self,user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def create_pending_user(self, phone, first_name, last_name, password):
        PendingUser.objects.update_or_create(phone=phone, defaults={
            "phone": phone, "first_name": first_name,
            "last_name": last_name, "password": password,
        })

    def send_confirmation(self, phone) -> bool:
        try:
            self.send_confirm(phone)
            return True
        except SmsException as e:
            ResponseException(e, data={"expired": e.kwargs.get("expired")})
        except Exception as e:
            ResponseException(e)

    def create_user_from_pending(self, pending_user):
        """Create user if user not found"""

        if User.objects.filter(phone=pending_user.phone).exists():
            ResponseException(_(Messages.USER_ALREADY_EXISTS), error_code=Codes.USER_ALREADY_EXISTS_ERROR)
        user = User.objects.create_user(phone=pending_user.phone, password=pending_user.password)
        user.first_name = pending_user.first_name
        user.last_name = pending_user.last_name
        user.save()
        token = self.get_token(user)
        return token

    def change_password(self, phone, password):
        """Change password"""

        user = User.objects.filter(phone=phone).first()
        user.set_password(password)
        user.save()
