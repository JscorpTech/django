from typing import Type

from django.utils.translation import gettext as _
from rest_framework import permissions, request, throttling, views, response

from core import services
from core.http import serializers


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
