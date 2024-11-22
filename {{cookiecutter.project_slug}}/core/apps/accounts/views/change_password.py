from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext as _
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import response, status, exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from ..serializers import ChangePasswordSerializer


class ChangePasswordView(APIView):
    """usaer password change view"""

    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        request=serializer_class,
        responses={200: OpenApiResponse(ChangePasswordSerializer)},
        summary="Change user password.",
        description="Change password of the authenticated user.",
    )
    def post(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        if user.check_password(request.data["old_password"]):
            user.password = make_password(request.data["new_password"])
            user.save()
            return response.Response(
                data={"detail": "password changed successfully"},
                status=status.HTTP_200_OK,
            )
        raise exceptions.PermissionDenied(
            _("invalida password"),
        )
