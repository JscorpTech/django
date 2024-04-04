from rest_framework import generics

from core.utils import response


class ListApiView(generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return response.ApiResponse().success(data=serializer.data)


class CreateApiView(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return response.ApiResponse().success(self.message if hasattr(self, "message") else "Successfully created")
