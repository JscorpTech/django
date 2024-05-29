from rest_framework import viewsets, permissions

from core.http import models
from core.http import serializers


class PostListView(viewsets.ModelViewSet):
    queryset = models.Post.objects.all()
    permissions = [permissions.AllowAny]
    serializer_class = serializers.PostSerializer

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
