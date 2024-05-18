from rest_framework import serializers

from core.http import models


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = ["title", "desc", "image"]


class FrontendTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FrontendTranslation
        fields = ["key", "value"]
