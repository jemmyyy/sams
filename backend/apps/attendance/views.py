from apps.permissions.permissions import IsCoach, IsOperations
from rest_framework import viewsets

from .models import Attendance
from .serializers import AttendanceSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsOperations | IsCoach]

    def perform_create(self, serializer):
        serializer.save(marked_by=self.request.user)
