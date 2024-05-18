"""
Raise exception
"""

from rest_framework import exceptions


class SmsException(Exception):
    """
    Sms exception
    """

    def __init__(self, message, **kwargs):
        super().__init__(message)
        self.kwargs = kwargs


class BreakException(Exception):
    """
    Break exception
    """

    def __init__(self, *args, message: str = None, data=None):
        if data is None:
            data = []
        self.args = args
        self.message = message
        self.data = data


class MyApiException(exceptions.APIException):
    """
    My API Exception for API exceptions status code edit
    """

    status_code = 400

    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code
