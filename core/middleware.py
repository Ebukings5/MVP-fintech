from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

class ValidateRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in ['POST', 'PUT']:
            if not request.content_type == 'application/json':
                logger.warning('Invalid Content-Type: %s', request.content_type)
                return JsonResponse({'error': 'Content-Type must be application/json'}, status=415)

            if not request.body:  # Check for empty request body
                logger.warning('Empty request body for %s', request.method)
                return JsonResponse({'error': 'Request body cannot be empty'}, status=400)

        response = self.get_response(request)
        return response

class YourMiddlewareClass:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Your middleware logic here
        response = self.get_response(request)
        return response