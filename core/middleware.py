from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger(__name__)

class ValidateRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info('Request received: %s %s', request.method, request.path)

        # Check if the request method requires a body (POST or PUT)
        if request.method in ['POST', 'PUT']:
            logger.info('Checking content type and body for %s', request.path)
            # Ensure the Content-Type is application/json
            if request.content_type != 'application/json':
                logger.warning('Invalid Content-Type for %s: %s', request.path, request.content_type)
                return JsonResponse({'error': 'Content-Type must be application/json'}, status=415)

            # Ensure the request body is not empty
            if not request.body:
                logger.warning('Empty request body for %s: %s', request.path, request.method)
                return JsonResponse({'error': 'Request body cannot be empty'}, status=400)

        response = self.get_response(request)
        return response


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Check if the path starts with '/api/' and the user is not authenticated
        if request.path.startswith('/api/') and not request.user.is_authenticated:
            logger.warning('Unauthenticated access attempt to %s', request.path)
            return JsonResponse({'error': 'Authentication required'}, status=401)
        return None


class LoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        logger.info('Request: %s %s', request.method, request.path)

    def process_response(self, request, response):
        logger.info('Response: %s %s', request.method, request.path)
        return response


# Custom middleware for future extension or additional logic
class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Add custom logic here (e.g., security checks, additional headers)
        response = self.get_response(request)
        return response


# CORS Middleware (for frontend-backend communication)
class CORSMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Add CORS headers to allow frontend (e.g., React) to communicate with Django
        response['Access-Control-Allow-Origin'] = '*'  # Allow all origins, or restrict to specific domains
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
