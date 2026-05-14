from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import SessionReport, GeneratedReport, ScheduledReport
from .serializers import SessionReportSerializer, GeneratedReportSerializer, ScheduledReportSerializer
from .tasks import generate_report_task
from apps.permissions.permissions import IsOperations

class SessionReportViewSet(viewsets.ModelViewSet):
    queryset = SessionReport.objects.all()
    serializer_class = SessionReportSerializer
    permission_classes = [permissions.IsAuthenticated] # Coaches can create reports

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
