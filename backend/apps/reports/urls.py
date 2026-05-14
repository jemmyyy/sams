from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SessionReportViewSet, GeneratedReportViewSet, ScheduledReportViewSet

router = DefaultRouter()
router.register(r'session-reports', SessionReportViewSet, basename='session-reports')
router.register(r'exports', GeneratedReportViewSet, basename='report-exports')
router.register(r'schedules', ScheduledReportViewSet, basename='report-schedules')

urlpatterns = [
    path('', include(router.urls)),
]
