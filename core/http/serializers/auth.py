from rest_framework import serializers
from rest_framework import validators

from core.http import models
from django.utils.translation import gettext as _

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class RegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=255, validators=[
        validators.UniqueValidator(queryset=models.User.objects.all())])

    class Meta:
        model = models.User
        fields = [
            "first_name", "last_name",
            "phone", "password"
        ]
        extra_kwargs = {
            "first_name": {
                "required": True,
            },
            "last_name": {
                "required": True
            }
        }


class ConfirmSerializer(serializers.Serializer):
    code = serializers.IntegerField(min_value=1000, max_value=9999)
    phone = serializers.CharField(max_length=255)


class PendingUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'phone', 'first_name', 'last_name']
        model = models.PendingUser


class ResetPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=255)

    def validate_phone(self, value):
        user = models.User.objects.filter(phone=value)
        if user.exists():
            return value

        raise serializers.ValidationError(_("User does not exist"))


class ResetConfirmationSerializer(serializers.Serializer):
    code = serializers.IntegerField(min_value=1000, max_value=9999)
    phone = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

    def validate_phone(self, value):
        user = models.User.objects.filter(phone=value)
        if user.exists():
            return value
        raise serializers.ValidationError(_("User does not exist"))


class ResendSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=255)
