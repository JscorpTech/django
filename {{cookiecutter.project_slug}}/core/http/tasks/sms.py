"""
Base celery tasks
"""

from celery import shared_task
from django.utils.translation import gettext as _

from core.utils import console
from importlib import import_module
from config.env import env


@shared_task
def SendConfirm(phone, code):
    try:
        service = getattr(
            import_module(env.str("OTP_MODULE")), env.str("OTP_SERVICE")
        )()
        service.send_sms(
            phone, _("Sizning Tasdiqlash ko'dingiz: %(code)s") % {"code": code}
        )
        console.Console().success(f"Success: {phone}-{code}")
    except Exception as e:
        console.Console().error(
            "Error: {phone}-{code}\n\n{error}".format(phone=phone, code=code, error=e)
        )  # noqa
        raise Exception("Sms yuborishda xatolik yuzaga keldi")
