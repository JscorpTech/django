from rest_framework import status
from rest_framework.response import Response

from core.exceptions import (
    BreakException
)


class ApiResponse:

    def response(self, success=True, message="", data=None, status_code=status.HTTP_200_OK, **kwargs):
        if data is None:
            data = {}
        response = {
            "success": success,
            "message": message,
            "data": data,
            **kwargs
        }
        return Response(data=response, status=status_code)

    def success(self, message="", data=None, status_code=status.HTTP_200_OK, **kwargs):
        return self.response(True, message, data, status_code, **kwargs)

    def error(self, message="", data=None, error_code=0, status_code=status.HTTP_400_BAD_REQUEST, exception=None,
              **kwargs):
        if isinstance(exception, BreakException):
            raise exception
        return self.response(False, message, data, status_code, error_code=error_code, **kwargs)
