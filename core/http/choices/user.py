from django.db import models


class RoleChoice(models.TextChoices):
    """
    User Role Choice
    """

    SUPERUSER = "superuser"
    ADMIN = "admin"
    USER = "user"
