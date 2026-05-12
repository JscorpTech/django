# type: ignore
"""
Base celery tasks
"""

import logging
import os
from importlib import import_module

from django.utils.translation import gettext as _

from config.env import env

try:
    from celery import shared_task
except ImportError:

    def shared_task(func):
        return func


@shared_task
def SendConfirm(phone, code):
    """Tasdiqlash ko'dini yuborish

    Args:
        phone (str, int): telefon no'mer
        code (str, int): tasdiqlash ko'di

    Raises:
        Exception: [TODO:description]
    """
    try:
        service = getattr(
            import_module(os.getenv("OTP_MODULE")), os.getenv("OTP_SERVICE")
        )()
        service.send_sms(
            phone, env.str("OTP_MESSAGE", _("Sizning Tasdiqlash ko'dingiz: %(code)s")) % {"code": code}
        )
        logging.info("Sms confirmation sent to phone ending with %s", str(phone)[-4:])
    except Exception as e:
        logging.error(
            "Sms provider error for phone ending with {phone_suffix}: {error}".format(
                phone_suffix=str(phone)[-4:],
                error=e,
            )
        )  # noqa
        raise Exception
