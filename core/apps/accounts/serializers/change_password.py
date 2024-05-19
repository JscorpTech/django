from rest_framework import serializers


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self):
        if self.context.get("request").user is None:
            raise serializers.ValidationError(
                {
                    "detail": "User not found.",
                }
            )
