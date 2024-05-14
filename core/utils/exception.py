from rest_framework import status

from core import exceptions


class ResponseException:

    def __init__(
        self,
        message="",
        data=None,
        error_code=0,
        status_code=status.HTTP_400_BAD_REQUEST,
        exception=None,
        **kwargs
    ):
        if isinstance(exception, exceptions.BreakException):
            raise exception

        if data is None:
            data = []
        response = {
            "success": False,
            "message": message,
            "data": data,
            "error_code": error_code,
            **kwargs
        }
        raise exceptions.MyApiException(response, status_code)
