from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import NotificationLog, UserNotificationPreference, ChannelChoices
from .serializers import NotificationLogSerializer, UserNotificationPreferenceSerializer


class NotificationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API for users to see their notifications (mostly In-App).
    """
    serializer_class = NotificationLogSerializer

    def get_queryset(self):
        # Users only see their own notifications, usually filtered by in-app for frontend
        return NotificationLog.objects.filter(
            user=self.request.user,
            channel=ChannelChoices.IN_APP
        ).order_by("-created_at")

    @action(detail=True, methods=["post"])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.read_at = timezone.now()
        notification.save()
        return Response({"status": "read"})

    @action(detail=False, methods=["post"])
    def mark_all_read(self, request):
        self.get_queryset().filter(read_at__isnull=True).update(read_at=timezone.now())
        return Response({"status": "all marked as read"})


class UserPreferenceViewSet(viewsets.ModelViewSet):
    """
    API for users to manage their notification preferences.
    """
    serializer_class = UserNotificationPreferenceSerializer

    def get_queryset(self):
        return UserNotificationPreference.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"])
    def defaults(self, request):
        # Return default preferences (all enabled) if not set in DB
        existing = {p.channel: p.is_enabled for p in self.get_queryset()}
        data = []
        for choice in ChannelChoices:
            data.append({
                "channel": choice.value,
                "is_enabled": existing.get(choice.value, True)
            })
        return Response(data)
