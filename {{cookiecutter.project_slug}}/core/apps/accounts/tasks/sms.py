"""
Base celery tasks
"""

import logging
import os
from importlib import import_module

from celery import shared_task
from config.env import env
from django.utils.translation import gettext as _


@shared_task
def SendConfirm(phone, code):
    try:
        service = getattr(
            import_module(os.getenv("OTP_MODULE")), os.getenv("OTP_SERVICE")
        )()
        service.send_sms(
            phone, env.str("OTP_MESSAGE", _("Sizning Tasdiqlash ko'dingiz: %(code)s")) % {"code": code}
        )
        logging.info("Sms send: %s-%s" % (phone, code))
    except Exception as e:
        logging.error(
            "Error: {phone}-{code}\n\n{error}".format(phone=phone, code=code, error=e)
        )  # noqa
        raise Exception
