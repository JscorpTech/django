from rest_framework import serializers


class SetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, write_only=True)
    token = serializers.CharField(max_length=255)
