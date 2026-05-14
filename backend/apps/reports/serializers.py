from rest_framework import serializers
from .models import SessionReport, GeneratedReport, ScheduledReport

class SessionReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionReport
        fields = "__all__"

class GeneratedReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedReport
        fields = [
            "id", 
            "report_type", 
            "format", 
            "status", 
            "file", 
            "error_message", 
            "parameters", 
            "requested_by", 
            "created_at"
        ]
        read_only_fields = ["id", "status", "file", "error_message", "requested_by", "created_at"]

class ScheduledReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledReport
        fields = "__all__"
