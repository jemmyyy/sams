from apps.permissions.permissions import IsCustomer
from django.utils import timezone
from rest_framework import viewsets

from .models import CancellationRequest
from .serializers import CancellationRequestSerializer


class CancellationRequestViewSet(viewsets.ModelViewSet):
    queryset = CancellationRequest.objects.all()
    serializer_class = CancellationRequestSerializer
    permission_classes = [IsCustomer]

    def perform_create(self, serializer):
        # Business Rule: Automated approval if requested > 24 hours before session
        occurrence = serializer.validated_data["occurrence"]
        deadline = occurrence.start_datetime - timezone.timedelta(hours=24)

        request_status = "pending"
        if timezone.now() < deadline:
            request_status = "approved"

        serializer.save(status=request_status)
