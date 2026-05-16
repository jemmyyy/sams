from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AttendanceAnalyticsViewSet,
    CoachPerformanceViewSet,
    EnrollmentAnalyticsViewSet,
    RevenueAnalyticsViewSet,
    SessionUtilizationViewSet,
)

router = DefaultRouter()
router.register(r'revenue', RevenueAnalyticsViewSet, basename='revenue-analytics')
router.register(r'attendance', AttendanceAnalyticsViewSet, basename='attendance-analytics')
router.register(r'enrollment', EnrollmentAnalyticsViewSet, basename='enrollment-analytics')
router.register(r'coach-performance', CoachPerformanceViewSet, basename='coach-performance-analytics')
router.register(r'utilization', SessionUtilizationViewSet, basename='utilization-analytics')

app_name = "analytics"

urlpatterns = [
    path('', include(router.urls)),
]
