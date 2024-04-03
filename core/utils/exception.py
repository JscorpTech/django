from rest_framework import status

from core.exceptions import BreakException, MyApiException


class ResponseException:

    def __init__(self, message="", data=None, error_code=0, status_code=status.HTTP_400_BAD_REQUEST, exception=None,
                 **kwargs):
        if isinstance(exception, BreakException):
            raise exception

        if data is None:
            data = []
        response = {
            "success": False, "message": message,
            "data": data, "error_code": error_code,
            **kwargs
        }
        raise MyApiException(response, status_code)
