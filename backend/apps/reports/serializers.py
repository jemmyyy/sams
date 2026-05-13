from rest_framework import serializers

from .models import SessionReport


class SessionReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionReport
        fields = "__all__"
        read_only_fields = ("academy", "coach", "submitted_at")
