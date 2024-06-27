from rest_framework import permissions, viewsets

from core.http import models, serializers


class PostListView(viewsets.ModelViewSet):
    queryset = models.Post.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.PostSerializer

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
