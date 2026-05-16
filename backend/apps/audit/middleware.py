from apps.common.thread_local import get_current_academy_id
from apps.audit.tasks import write_audit_log


class AuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not request.path.startswith("/api/"):
            return response

        actor_id = str(request.user.id) if request.user.is_authenticated else None
        academy_id = get_current_academy_id()

        write_audit_log.delay(
            actor_id=actor_id,
            academy_id=academy_id,
            action=self._map_method(request.method),
            entity_type="http_request",
            entity_id=request.path,
            ip_address=request.META.get("REMOTE_ADDR"),
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
            metadata={
                "status_code": response.status_code,
                "method": request.method,
                "query_string": request.META.get("QUERY_STRING", ""),
            },
        )
        return response

    @staticmethod
    def _map_method(method):
        mapping = {"POST": "create", "PUT": "update", "PATCH": "update", "DELETE": "delete"}
        return mapping.get(method, "create")
