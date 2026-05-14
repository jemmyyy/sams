from rest_framework import serializers
from .models import NotificationLog, UserNotificationPreference


class NotificationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationLog
        fields = [
            "id",
            "channel",
            "status",
            "subject",
            "content",
            "created_at",
            "read_at",
        ]
        read_only_fields = fields


class UserNotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotificationPreference
        fields = ["channel", "is_enabled"]
