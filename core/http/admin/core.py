"""
Admin panel register
"""

from django.contrib import admin
from django.contrib.auth import models as db_models

from core.http import models
from core.http.admin import user
from core.http.admin import another

admin.site.unregister(db_models.Group)
admin.site.register(db_models.Group, user.GroupAdmin)

admin.site.register(models.Tags, another.TagsAdmin)
admin.site.register(models.Post, another.PostAdmin)
admin.site.register(models.User, user.CustomUserAdmin)
admin.site.register(models.Comment, another.CommentAdmin)
admin.site.register(models.SmsConfirm, another.SmsConfirmAdmin)
admin.site.register(
    models.FrontendTranslation, another.FrontendTranslationAdmin
)  # noqa
