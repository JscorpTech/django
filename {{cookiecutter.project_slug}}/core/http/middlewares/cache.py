class CacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        vary_headers = set(response.get("Vary", "").replace(" ", "").split(","))
        vary_headers.update(["Accept-Language"])
        # Authorization
        response["Vary"] = ", ".join(vary_headers)
        return response
