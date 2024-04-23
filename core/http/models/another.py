from django.db import models
from polymorphic import models as polymorphic
from django.utils.translation import gettext as _


class Tags(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class Comment(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.text


class BaseComment(polymorphic.PolymorphicModel):
    comments = models.ManyToManyField(Comment)


class Post(BaseComment):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True)
    tags = models.ManyToManyField(Tags)

    def __str__(self):
        return self.title


class FrontendTranslation(models.Model):
    key = models.CharField(max_length=255, unique=True)
    value = models.TextField()

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = _("Frontend Translation")
        verbose_name_plural = _("Frontend Translations")
