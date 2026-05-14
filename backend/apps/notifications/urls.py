from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, UserPreferenceViewSet

router = DefaultRouter()
router.register(r"my-notifications", NotificationViewSet, basename="my-notifications")
router.register(r"preferences", UserPreferenceViewSet, basename="notification-preferences")

urlpatterns = [
    path("", include(router.urls)),
]
