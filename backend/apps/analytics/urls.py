from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RevenueAnalyticsViewSet, 
    AttendanceAnalyticsViewSet, 
    EnrollmentAnalyticsViewSet, 
    CoachPerformanceViewSet
)

router = DefaultRouter()
router.register(r'revenue', RevenueAnalyticsViewSet, basename='revenue-analytics')
router.register(r'attendance', AttendanceAnalyticsViewSet, basename='attendance-analytics')
router.register(r'enrollment', EnrollmentAnalyticsViewSet, basename='enrollment-analytics')
router.register(r'coach-performance', CoachPerformanceViewSet, basename='coach-performance-analytics')

app_name = "analytics"

urlpatterns = [
    path('', include(router.urls)),
]
