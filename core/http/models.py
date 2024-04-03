#####################
# Project base models
#####################

from datetime import datetime, timedelta, timezone

import math
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel

from common.env import env
from core.http.managers import UserManager


class User(AbstractUser):
    phone = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    USERNAME_FIELD = u"phone"

    objects = UserManager()

    def __str__(self):
        return self.phone


class Tags(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _("Tags")
        verbose_name = _("Tag")


class PendingUser(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.phone)}"

    def is_valid(self) -> bool:
        """10 mins OTP validation"""
        lifespan_in_seconds = float(env("OTP_EXPIRE_TIME") * 60)
        now = datetime.now(timezone.utc)
        time_diff = now - self.created_at
        time_diff = time_diff.total_seconds()
        if time_diff >= lifespan_in_seconds:
            return False
        return True


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


class Comment(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.text


class BaseComment(PolymorphicModel):
    comments = models.ManyToManyField(Comment)


class Post(BaseComment):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True)
    tags = models.ManyToManyField(Tags)

    def __str__(self):
        return self.title


class FrontendTranslation(BaseComment):
    key = models.CharField(max_length=255, unique=True)
    value = models.TextField()

    def __str__(self):
        return self.key

    class Meta:
        verbose_name_plural = _("Frontend Translations")
        verbose_name = _("Frontend Translation")
