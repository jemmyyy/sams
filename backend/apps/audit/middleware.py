import logging
from django.utils import timezone
from apps.common.thread_local import get_current_academy_id

logger = logging.getLogger(__name__)

class AuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Basic audit logging - in a real scenario, this would be a task sent to Celery
        # to save into an AuditLog model.
        if request.user.is_authenticated:
            user = request.user.username
        else:
            user = "Anonymous"
            
        academy_id = get_current_academy_id()
        
        logger.info(
            f"AUDIT: User: {user} | Academy: {academy_id} | "
            f"Method: {request.method} | Path: {request.path} | Status: {response.status_code}"
        )
        
        return response
