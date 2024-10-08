"""
Admin panel register
"""

from django.contrib import admin
from django.contrib.auth import models as db_models

from core.http import models
from core.http.admin import user
from .user import SmsConfirmAdmin

admin.site.unregister(db_models.Group)
admin.site.register(db_models.Group, user.GroupAdmin)

admin.site.register(models.User, user.CustomUserAdmin)
admin.site.register(models.SmsConfirm, SmsConfirmAdmin)
