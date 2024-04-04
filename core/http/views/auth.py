from rest_framework import views, throttling, request

from core import utils, enums, services
from core.http import serializers
from django.utils.translation import gettext as _


class AbstractSendSms(views.APIView):
    serializer_class = serializers.ResendSerializer
    throttle_classes = [throttling.UserRateThrottle]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = services.UserService()

    def post(self, request: request.Request):
        ser = self.serializer_class(data=request.data)
        ser.is_valid(raise_exception=True)
        phone = ser.data.get('phone')
        self.service.send_confirmation(phone)
        return utils.ApiResponse().success(_(enums.Messages.SEND_MESSAGE) % {'phone': phone})
