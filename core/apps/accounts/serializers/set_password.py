from rest_framework import serializers


class SetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    token = serializers.CharField(max_length=255)
