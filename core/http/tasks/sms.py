"""
Base celery tasks
"""
from celery import shared_task
from django.utils.translation import gettext as _

from core.utils import console
from core.services import sms_service


@shared_task
def SendConfirm(phone, code):
    try:
        service: sms_service.SendService = sms_service.SendService()
        service.send_sms(phone, _("Sizning Tasdiqlash ko'dingiz: %(code)s") % {
            'code': code})
        console.Console().success(
            "Success: {phone}-{code}".format(phone=phone, code=code))
    except Exception as e:
        console.Console().error("Error: {phone}-{code}\n\n{error}".format(phone=phone, code=code, error=e)) # noqa
