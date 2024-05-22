class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(
            f"""Request: {request.method} {request.path} from {request.META['REMOTE_ADDR']}"""
        )

        response = self.get_response(request)

        print(f"Response: {response.status_code}")

        return response
