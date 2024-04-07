from datetime import datetime, timezone, timedelta

import math
from django.contrib.auth import models as auth_models
from django.db import models

from common.env import env
from core.http import managers


class User(auth_models.AbstractUser):
    phone = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)  # User created at time
    updated_at = models.DateTimeField(auto_now=True)  # User updated at time
    validated_at = models.DateTimeField(null=True, blank=True)  # User validated at time

    USERNAME_FIELD = u"phone"

    objects = managers.UserManager()

    def __str__(self):
        return self.phone




class SmsConfirm(models.Model):
    SMS_EXPIRY_SECONDS = 120
    RESEND_BLOCK_MINUTES = 10
    TRY_BLOCK_MINUTES = 2
    RESEND_COUNT = 5
    TRY_COUNT = 10

    code = models.IntegerField()
    try_count = models.IntegerField(default=0)
    resend_count = models.IntegerField(default=0)
    phone = models.CharField(max_length=20)
    expire_time = models.DateTimeField(null=True, blank=True)
    unlock_time = models.DateTimeField(null=True, blank=True)
    resend_unlock_time = models.DateTimeField(null=True, blank=True)

    def sync_limits(self):
        if self.resend_count >= self.RESEND_COUNT:
            self.try_count = 0
            self.resend_count = 0
            self.resend_unlock_time = datetime.now() + timedelta(
                minutes=self.RESEND_BLOCK_MINUTES)
        elif self.try_count >= self.TRY_COUNT:
            self.try_count = 0
            self.unlock_time = datetime.now() + timedelta(
                minutes=self.TRY_BLOCK_MINUTES)

        if self.resend_unlock_time is not None and \
                self.resend_unlock_time.timestamp() \
                < datetime.now().timestamp():
            self.resend_unlock_time = None

        if self.unlock_time is not None and self.unlock_time.timestamp() \
                < datetime.now().timestamp():
            self.unlock_time = None
        self.save()

    def is_expired(self):
        return self.expire_time.timestamp() < datetime.now().timestamp() if \
            hasattr(
                self.expire_time,
                "timestamp") else None

    def is_block(self):
        return self.unlock_time is not None

    def reset_limits(self):
        self.try_count = 0
        self.resend_count = 0
        self.unlock_time = None

    def interval(self, time):
        expire = time.timestamp() - datetime.now().timestamp()
        minutes = math.floor(expire / 60)
        expire -= minutes * 60
        expire = math.floor(expire)

        return '{:02d}:{:02d}'.format(minutes, expire)

    def __str__(self) -> str:
        return "{phone} | {code}".format(phone=self.phone,
                                         code=self.code)