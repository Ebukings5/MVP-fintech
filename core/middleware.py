# core/middleware.py

from django.http import JsonResponse

class ValidateRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in ['POST', 'PUT']:
            if not request.content_type == 'application/json':
                return JsonResponse({'error': 'Content-Type must be application/json'}, status=415)
            # Add more global validation checks as needed

        response = self.get_response(request)
        return response
class YourMiddlewareClass:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Your middleware logic here
        response = self.get_response(request)
        return response