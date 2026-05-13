from apps.permissions.permissions import IsOperations
from rest_framework import viewsets

from .models import Announcement
from .serializers import AnnouncementSerializer


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsOperations]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
