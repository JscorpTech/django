from rest_framework import viewsets

from core.http.models import Post
from core.http.serializers import PostSerializer


class PostListView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
