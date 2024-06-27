from typing import Type

from django.utils.translation import gettext as _
from rest_framework import permissions, request, throttling, views

from core import enums, services
from core.http import serializers
from core.http.views import generics as http_views


class AbstractSendSms(views.APIView, http_views.ApiResponse):
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
        return self.success(_(enums.Messages.SEND_MESSAGE) % {"phone": phone})
