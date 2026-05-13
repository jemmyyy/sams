from apps.permissions.permissions import IsCoach, IsOperations
from rest_framework import viewsets

from .models import SessionReport
from .serializers import SessionReportSerializer


class SessionReportViewSet(viewsets.ModelViewSet):
    queryset = SessionReport.objects.all()
    serializer_class = SessionReportSerializer
    permission_classes = [IsCoach | IsOperations]

    def perform_create(self, serializer):
        serializer.save(coach=self.request.user)
