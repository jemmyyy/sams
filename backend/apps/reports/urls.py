from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SessionReportViewSet

router = DefaultRouter()
router.register(r'', SessionReportViewSet)

app_name = 'reports'

urlpatterns = [
    path('', include(router.urls)),
]
