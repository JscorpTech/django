from django.db import models
from django.utils.translation import gettext as _
from core.http.models import AbstractBaseModel


class Tags(AbstractBaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class Post(AbstractBaseModel):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    image = models.ImageField(upload_to="posts/", blank=True)
    tags = models.ManyToManyField(Tags)

    def __str__(self):
        return self.title


class Comment(AbstractBaseModel):
    text = models.CharField(max_length=255)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.text
