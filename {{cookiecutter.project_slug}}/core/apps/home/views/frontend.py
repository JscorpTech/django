"""
Admin panel UI view
"""

from rest_framework import generics, permissions, status
from ..models import FrontendTranslation
from ..serializers import FrontendTransactionSerializer
from rest_framework.response import Response


class FrontendTranslationView(generics.ListAPIView):
    queryset = FrontendTranslation.objects.all()
    serializer_class = FrontendTransactionSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        data = {}

        for obj in serializer.data:
            data[obj["key"]] = obj["value"]
        return Response(data=data, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = self.queryset.all()
        key = self.request.GET.get("key")

        if key:
            queryset = queryset.filter(key__icontains=key)

        return queryset
