from rest_framework import serializers
from .models import (
    CoachPerformanceSnapshot,
    DailyAttendanceSnapshot,
    DailyRevenueSnapshot,
    MonthlyEnrollmentSnapshot,
    SessionUtilizationSnapshot,
)

class DailyRevenueSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyRevenueSnapshot
        fields = ["date", "total_income", "total_refunds", "net_revenue", "payment_count"]

class DailyAttendanceSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyAttendanceSnapshot
        fields = ["date", "total_expected", "total_present", "total_absent", "attendance_rate"]

class MonthlyEnrollmentSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyEnrollmentSnapshot
        fields = ["year", "month", "total_active_players", "new_enrollments", "churned_players", "retention_rate"]


class SessionUtilizationSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionUtilizationSnapshot
        fields = ["date", "total_occurrences", "completed", "cancelled", "total_enrollment_capacity", "total_enrolled", "utilization_rate"]

class CoachPerformanceSnapshotSerializer(serializers.ModelSerializer):
    coach_name = serializers.CharField(source="coach.get_full_name", read_only=True)
    class Meta:
        model = CoachPerformanceSnapshot
        fields = [
            "coach", 
            "coach_name", 
            "period_start", 
            "period_end", 
            "sessions_conducted", 
            "average_attendance_rate", 
            "reports_submitted"
        ]
