from rest_framework import viewsets, status
from rest_framework.response import Response
from apps.permissions.permissions import IsOperations, IsCoach
from ..models import Attendance
from ..serializers import AttendanceSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsOperations | IsCoach]

    def perform_create(self, serializer):
        serializer.save(marked_by=self.request.user)
