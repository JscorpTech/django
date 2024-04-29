import uuid

from django.db import models

from config import settings
from core.http.models import User


class ResetToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.token

    class Meta:
        verbose_name = 'Reset Token'
        verbose_name_plural = 'Reset Tokens'
