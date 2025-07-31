import random
from datetime import datetime, timedelta

from config.env import env
from core.apps.accounts.tasks.sms import SendConfirm
from django_core import exceptions, models


class SmsService:
    @staticmethod
    def send_confirm(phone):
        # TODO: Deploy this change when deploying -> code = random.randint(1000, 9999) # noqa
        if env.bool("OTP_PROD", False):
            code = "".joint(random.randint(0, 9) for _ in range(env.int("OTP_SIZE", 4)))
        else:
            code = env.int("OTP_DEFAULT", 1111) 

        sms_confirm, status = models.SmsConfirm.objects.get_or_create(phone=phone, defaults={"code": code})

        sms_confirm.sync_limits()

        if sms_confirm.resend_unlock_time is not None:
            expired = sms_confirm.interval(sms_confirm.resend_unlock_time)
            exception = exceptions.SmsException(f"Resend blocked, try again in {expired}", expired=expired)
            raise exception

        sms_confirm.code = code
        sms_confirm.try_count = 0
        sms_confirm.resend_count += 1
        sms_confirm.phone = phone
        sms_confirm.expired_time = datetime.now() + timedelta(seconds=models.SmsConfirm.SMS_EXPIRY_SECONDS)  # noqa
        sms_confirm.resend_unlock_time = datetime.now() + timedelta(
            seconds=models.SmsConfirm.SMS_EXPIRY_SECONDS
        )  # noqa
        sms_confirm.save()

        SendConfirm.delay(phone, code)
        return True

    @staticmethod
    def check_confirm(phone, code):
        sms_confirm = models.SmsConfirm.objects.filter(phone=phone).first()

        if sms_confirm is None:
            raise exceptions.SmsException("Invalid confirmation code")

        sms_confirm.sync_limits()

        if sms_confirm.is_expired():
            raise exceptions.SmsException("Time for confirmation has expired")

        if sms_confirm.is_block():
            expired = sms_confirm.interval(sms_confirm.unlock_time)
            raise exceptions.SmsException(f"Try again in {expired}")

        if str(sms_confirm.code) == str(code):
            sms_confirm.delete()
            return True

        sms_confirm.try_count += 1
        sms_confirm.save()

        raise exceptions.SmsException("Invalid confirmation code")
