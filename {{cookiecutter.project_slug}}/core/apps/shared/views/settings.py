from django_core.mixins import BaseViewSetMixin
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from django.conf import settings
from rest_framework.response import Response
from ..serializers import ListLanguageSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse


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
