from apps.permissions.permissions import IsCustomer, IsOperations
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import CancellationPolicy, CancellationRequest
from .serializers import CancellationPolicySerializer, CancellationRequestSerializer


class CancellationPolicyViewSet(viewsets.ModelViewSet):
    queryset = CancellationPolicy.objects.all()
    serializer_class = CancellationPolicySerializer
    permission_classes = [IsOperations]


class CancellationRequestViewSet(viewsets.ModelViewSet):
    queryset = CancellationRequest.objects.all()
    serializer_class = CancellationRequestSerializer
    permission_classes = [IsCustomer]

    def perform_create(self, serializer):
        occurrence = serializer.validated_data["occurrence"]
        request_status = "pending"

        try:
            policy = CancellationPolicy.objects.get(academy=occurrence.academy)
            auto_approve, _ = policy.evaluate_auto_approval(
                CancellationRequest(occurrence=occurrence)
            )
            if auto_approve:
                request_status = "approved"
        except CancellationPolicy.DoesNotExist:
            # Fallback: approve if more than 24 hours before session
            deadline = occurrence.start_datetime - timezone.timedelta(hours=24)
            if timezone.now() < deadline:
                request_status = "approved"

        serializer.save(status=request_status)

    @action(detail=True, methods=["post"])
    def review(self, request, pk=None):
        cancellation = self.get_object()
        new_status = request.data.get("status")
        if new_status not in ("approved", "rejected"):
            return Response({"error": "Status must be approved or rejected."}, status=400)
        cancellation.status = new_status
        cancellation.reviewed_by = request.user
        cancellation.review_notes = request.data.get("review_notes", "")
        cancellation.save()
        return Response(CancellationRequestSerializer(cancellation).data)
