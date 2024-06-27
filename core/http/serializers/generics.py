from rest_framework import exceptions, serializers

from core import enums
from core.utils import exception


class GenericSerializer(serializers.Serializer):
    def to_internal_value(self, data):
        try:
            return super().to_internal_value(data)
        except exceptions.ValidationError as e:
            key, value = next(iter(e.detail.items()))
            exception.ResponseException(
                value[0], error_code=enums.Codes.INVALID_PARAMETER_VALUE
            )
