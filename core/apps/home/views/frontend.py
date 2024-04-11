from rest_framework import status
from rest_framework.generics import ListAPIView

from core.http import views
from core.http.models import FrontendTranslation
from core.http.serializers import FrontendTransactionSerializer


class FrontendTranslationView(ListAPIView, views.ApiResponse):
    queryset = FrontendTranslation.objects.all()
    serializer_class = FrontendTransactionSerializer

    def get(self, request, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        data = {}

        for obj in serializer.data:
            data[obj["key"]] = obj["value"]
        return self.success(data=data, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = self.queryset.all()
        key = self.request.GET.get("key")

        if key:
            queryset = queryset.filter(key__icontains=key)

        return queryset
