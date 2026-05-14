from rest_framework import serializers
from .models import (
    DailyRevenueSnapshot, 
    DailyAttendanceSnapshot, 
    MonthlyEnrollmentSnapshot, 
    CoachPerformanceSnapshot
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
        fields = ["year", "month", "total_active_players", "new_enrollments", "churned_players"]

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
