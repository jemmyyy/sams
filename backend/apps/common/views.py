from django.db import connections
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        db_ok = True
        try:
            connections["default"].cursor()
        except Exception:
            db_ok = False

        redis_ok = True
        try:
            r = get_redis_connection("default")
            r.ping()
        except Exception:
            redis_ok = False

        overall = db_ok and redis_ok
        return Response(
            {
                "status": "healthy" if overall else "degraded",
                "database": "up" if db_ok else "down",
                "redis": "up" if redis_ok else "down",
            },
            status=status.HTTP_200_OK if overall else status.HTTP_503_SERVICE_UNAVAILABLE,
        )
