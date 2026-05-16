from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CoachAvailabilityViewSet, CoachViewSet

router = DefaultRouter()
router.register(r"profiles", CoachViewSet)

app_name = "coaches"

urlpatterns = [
    path("", include(router.urls)),
    path(
        "profiles/<uuid:coach_pk>/availabilities/",
        CoachAvailabilityViewSet.as_view({"get": "list", "post": "create"}),
        name="coach-availability-list",
    ),
    path(
        "profiles/<uuid:coach_pk>/availabilities/<uuid:pk>/",
        CoachAvailabilityViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}),
        name="coach-availability-detail",
    ),
]
