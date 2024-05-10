from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework import status

from django.contrib.auth.hashers import make_password

from core.http import views as http_views
from ..serializers import ChangePasswordSerializer


class ChangePasswordView(APIView, http_views.ApiResponse):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        if user is None:
            raise ValidationError(
                {
                    "success": True,
                    "message": "User not found.",
                }
            )
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            if user.check_password(request.data['old_password']):
                user.password = make_password(request.data['new_password'])
                user.save()
                return http_views.ApiResponse().success("password changed successfully", status_code=status.HTTP_200_OK)
            return http_views.ApiResponse().error("wrong old password", status_code=status.HTTP_400_BAD_REQUEST)
        return http_views.ApiResponse().error(serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)
