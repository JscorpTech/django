from django.http import JsonResponse

from core.exceptions import BreakException


class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except BreakException as e:
            return self.response(request, e)
        return response

    def response(self, request, e):
        error_data = {
            'message': e.message,
            "data": e.data,
            "errors": [
                e.args.__str__(),
            ]
        }
        return JsonResponse(error_data, status=500)
