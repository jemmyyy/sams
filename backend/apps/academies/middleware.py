from django.http import JsonResponse
from apps.common.thread_local import set_current_academy_id, clear_current_academy_id
from apps.academies.models import Academy

class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Extract tenant ID from header
        academy_id = request.headers.get("X-Academy-ID")
        
        # 2. Extract from domain if header is missing (e.g. for subdomains)
        if not academy_id:
            host = request.get_host().split(':')[0]
            # Simple domain lookup - could be cached in Redis
            academy = Academy.objects.filter(domain=host).first()
            if academy:
                academy_id = str(academy.id)

        # 3. Validation: If ID is provided, verify it exists and is active
        if academy_id:
            try:
                # Optimized check - existence only
                if not Academy.objects.filter(id=academy_id, is_active=True).exists():
                    return JsonResponse({
                        "success": False,
                        "message": "Invalid or inactive academy.",
                        "data": None,
                        "errors": {"academy": "Academy not found"}
                    }, status=404)
                
                set_current_academy_id(academy_id)
            except Exception:
                return JsonResponse({
                    "success": False,
                    "message": "Invalid academy ID format.",
                    "data": None,
                    "errors": {"academy": "Invalid UUID"}
                }, status=400)
        
        response = self.get_response(request)
        
        clear_current_academy_id()
        
        return response
