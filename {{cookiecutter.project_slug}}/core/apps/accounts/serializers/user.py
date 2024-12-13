from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["first_name", "last_name", "phone"]
        model = get_user_model()
