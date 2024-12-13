from core.http.models import AbstractBaseModel
from django.contrib.auth import get_user_model
from django.db import models


class ResetToken(AbstractBaseModel):
    token = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.token

    class Meta:
        verbose_name = "Reset Token"
        verbose_name_plural = "Reset Tokens"
