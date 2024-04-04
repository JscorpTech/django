#####################
# Version v1
#####################

from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView

from core.http.models import Post, FrontendTranslation
from core.http.serializers import PostSerializer, FrontendTransactionSerializer
from core.utils.response import ApiResponse


class PostListView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class FrontendTranslationView(ListAPIView):
    queryset = FrontendTranslation.objects.all()
    serializer_class = FrontendTransactionSerializer

    def get(self, request, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        data = {}

        for obj in serializer.data:
            data[obj["key"]] = obj["value"]
        return ApiResponse().success(data=data, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = self.queryset.all()
        key = self.request.GET.get("key")

        if key:
            queryset = queryset.filter(key__icontains=key)

        return queryset
