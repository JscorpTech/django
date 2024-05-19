from rest_framework import exceptions
from rest_framework import serializers

from django.utils.translation import gettext as _

from core.http import models


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class RegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=255)

    def validate_phone(self, value):
        user = models.User.objects.filter(
            phone=value, validated_at__isnull=False
        )
        if user.exists():
            return exceptions.ValidationError(
                _("Phone number already registered."), code="unique"
            )
        return value

    class Meta:
        model = models.User
        fields = ["first_name", "last_name", "phone", "password"]
        extra_kwargs = {
            "first_name": {
                "required": True,
            },
            "last_name": {"required": True},
        }


class ConfirmSerializer(serializers.Serializer):
    code = serializers.IntegerField(min_value=1000, max_value=9999)
    phone = serializers.CharField(max_length=255)


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

    def validate_phone(self, value):
        user = models.User.objects.filter(phone=value)
        if user.exists():
            return value
        raise serializers.ValidationError(_("User does not exist"))


class ResendSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=255)
