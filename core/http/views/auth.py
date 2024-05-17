from django.utils.translation import gettext as _
from rest_framework import views, permissions
from rest_framework import request
from rest_framework import throttling

from core import enums
from core import services
from core.http import serializers
from core.http.views import generics as http_views


class AbstractSendSms(views.APIView, http_views.ApiResponse):
    serializer_class = serializers.ResendSerializer
    throttle_classes = [throttling.UserRateThrottle]
    permission_classes = [permissions.AllowAny]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = services.UserService()

    def post(self, request: request.Request):
        ser = self.serializer_class(data=request.data)
        ser.is_valid(raise_exception=True)
        phone = ser.data.get('phone')
        self.service.send_confirmation(phone)
        return self.success(_(enums.Messages.SEND_MESSAGE) % {'phone': phone})
