from rest_framework import serializers
from ..models import FrontendTranslation


class FrontendTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrontendTranslation
        fields = ["key", "value"]
