"""
Raise exception
"""


class SmsException(Exception):
    """
    Sms exception
    """

    def __init__(self, message, **kwargs):
        super().__init__(message)
        self.kwargs = kwargs
