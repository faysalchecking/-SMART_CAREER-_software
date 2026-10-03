import logging
from django.utils.deprecation import MiddlewareMixin
from .models import AuditLog

logger = logging.getLogger(__name__)

class AuditLoggingMiddleware(MiddlewareMixin):
    """Middleware to log all API requests and responses"""
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Store request info for later logging
        request._audit_start_time = __import__('time').time()
        return None
    
    def process_response(self, request, response):
        # Log the request/response
        if hasattr(request, 'user') and request.user.is_authenticated:
            try:
                AuditLog.objects.create(
                    user=request.user,
                    action=request.method,
                    resource=request.path,
                    status_code=response.status_code,
                )
            except Exception as e:
                logger.error(f"Audit logging error: {str(e)}")
        
        return response