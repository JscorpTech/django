from rest_framework import serializers

from core.http import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["first_name", "last_name", "phone"]
        model = models.User
