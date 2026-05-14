from rest_framework import viewsets, permissions
from .models import (
    DailyRevenueSnapshot, 
    DailyAttendanceSnapshot, 
    MonthlyEnrollmentSnapshot, 
    CoachPerformanceSnapshot
)
from .serializers import (
    DailyRevenueSnapshotSerializer, 
    DailyAttendanceSnapshotSerializer, 
    MonthlyEnrollmentSnapshotSerializer, 
    CoachPerformanceSnapshotSerializer
)
from apps.permissions.permissions import IsOperations

class RevenueAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DailyRevenueSnapshot.objects.all()
    serializer_class = DailyRevenueSnapshotSerializer
    permission_classes = [IsOperations]
    filterset_fields = {"date": ["gte", "lte"]}

class AttendanceAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DailyAttendanceSnapshot.objects.all()
    serializer_class = DailyAttendanceSnapshotSerializer
    permission_classes = [IsOperations]
    filterset_fields = {"date": ["gte", "lte"]}

class EnrollmentAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MonthlyEnrollmentSnapshot.objects.all()
    serializer_class = MonthlyEnrollmentSnapshotSerializer
    permission_classes = [IsOperations]
    filterset_fields = ["year", "month"]

class CoachPerformanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CoachPerformanceSnapshot.objects.all()
    serializer_class = CoachPerformanceSnapshotSerializer
    permission_classes = [IsOperations]
    filterset_fields = ["coach", "period_start", "period_end"]
