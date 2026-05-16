from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.permissions.permissions import IsCoach, IsOperations

from .models import GeneratedReport, ScheduledReport, SessionReport
from .serializers import (
    GeneratedReportSerializer,
    ScheduledReportSerializer,
    SessionReportSerializer,
)
from .tasks import generate_report_task

class SessionReportViewSet(viewsets.ModelViewSet):
    queryset = SessionReport.objects.all()
    serializer_class = SessionReportSerializer
    permission_classes = [IsCoach]

class GeneratedReportViewSet(viewsets.ModelViewSet):
    queryset = GeneratedReport.objects.all()
    serializer_class = GeneratedReportSerializer
    permission_classes = [IsOperations]

    def perform_create(self, serializer):
        report = serializer.save(requested_by=self.request.user)
        generate_report_task.delay(str(report.id))

    @action(detail=True, methods=["post"])
    def retry(self, request, pk=None):
        report = self.get_object()
        if report.status == "failed":
            report.status = "pending"
            report.save()
            generate_report_task.delay(str(report.id))
            return Response({"status": "retrying"})
        return Response({"error": "Only failed reports can be retried"}, status=status.HTTP_400_BAD_REQUEST)

class ScheduledReportViewSet(viewsets.ModelViewSet):
    queryset = ScheduledReport.objects.all()
    serializer_class = ScheduledReportSerializer
    permission_classes = [IsOperations]
