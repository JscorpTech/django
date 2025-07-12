from django_core.mixins import BaseViewSetMixin
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from django.conf import settings
from rest_framework.response import Response
from ..serializers import ListLanguageSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse
from core.apps.shared.models import SettingsModel


@extend_schema(tags=["settings"])
class SettingsView(BaseViewSetMixin, GenericViewSet):
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ["languages"]:
            return ListLanguageSerializer
        return ListLanguageSerializer

    @extend_schema(responses={200: OpenApiResponse(response=ListLanguageSerializer(many=True))})
    @action(methods=["GET"], detail=False, url_path="languages", url_name="languages")
    def languages(self, request):
        return Response(self.get_serializer(settings.JST_LANGUAGES, many=True).data)

    @extend_schema(
        summary="Get public settings",
        responses={
            200: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "example_key": {
                            "type": "object",
                            "properties": {
                                "example_key": {"type": "array", "items": {"type": "string"}, "example": [12300.50]}
                            },
                        }
                    },
                }
            )
        },
    )
    @action(methods=["GET"], detail=False, url_path="config", url_name="config")
    def config(self, request):
        config = SettingsModel.objects.filter(is_public=True)
        response = {}
        for item in config:
            config_value = {}
            for option in item.options.all():
                config_value[option.key] = option.value
            response[item.key] = config_value
        return Response(data=response)
