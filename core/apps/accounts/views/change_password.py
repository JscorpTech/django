from django.contrib.auth.hashers import make_password

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework import status

from core.http import views as http_views
from ..serializers import ChangePasswordSerializer


class ChangePasswordView(APIView, http_views.ApiResponse):
    """usaer password change view"""
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)
    
    @swagger_auto_schema(
            request_body=serializer_class,
            responses={
                status.HTTP_200_OK: openapi.Response("Password changed successfully"),
                status.HTTP_400_BAD_REQUEST: openapi.Response("Bad request")
            },
            operation_summary="Change user password.",
            operation_description="Change password of the authenticated user."
    )   
    def post(self, request, *args, **kwargs):
        user = self.request.user
        if user is None:
            raise ValidationError(
                {
                    "success": True,
                    "message": "User not found.",
                }
            )
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if user.check_password(request.data['old_password']):
                user.password = make_password(request.data['new_password'])
                user.save()
                return http_views.ApiResponse().success("password changed successfully", status_code=status.HTTP_200_OK)
            return http_views.ApiResponse().error("wrong old password", status_code=status.HTTP_400_BAD_REQUEST)
        return http_views.ApiResponse().error(serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)
