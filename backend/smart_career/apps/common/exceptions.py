from rest_framework.views import exception_handler
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides consistent error responses
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        # Return custom error format
        return Response({
            'success': False,
            'error': response.data if isinstance(response.data, str) else response.data.get('detail', str(response.data)),
            'status': response.status_code,
        }, status=response.status_code)

    # Log unexpected errors
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return Response({
        'success': False,
        'error': 'An unexpected error occurred. Please try again.',
        'status': 500,
    }, status=500)