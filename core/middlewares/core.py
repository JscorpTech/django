from django.http import response

from core import exceptions


class ExceptionMiddleware:
    """
    This class is used to handle exceptions that occur during the request/\
        response cycle.
    It is a middleware that is added to the Django middleware pipeline.
    """

    def __init__(self, get_response):
        """
        Initialize the middleware.

        Args:
            get_response: The next middleware in the pipeline.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        This method is called for each request.
        It retrieves the response from the next middleware in the pipeline,
        and handles any exceptions that occur.

        Args:
            request: The incoming request.

        Returns:
            The response from the next middleware in the pipeline.
        """
        try:
            response = self.get_response(request)
        except exceptions.BreakException as e:
            return self.process_exception(request, e)
        return response

    def process_exception(self, request, e):
        """
        Process an exception that occurred during the request/response cycle.

        Args:
            request: The incoming request.
            e: The exception that occurred.

        Returns:
            A JSON response containing information about the exception.
        """
        if isinstance(e, exceptions.BreakException):
            """
            If the exception is a BreakException, construct a JSON response \
                containing the error message, data, and
            any additional arguments passed to the BreakException.
            """
            error_data = {
                "message": e.message,
                "data": e.data,
                "errors": [
                    e.args.__str__(),
                ],
            }
            return response.JsonResponse(error_data)
