from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.session import SessionOccurrenceViewSet, SessionSeriesViewSet, VenueViewSet

router = DefaultRouter()
router.register(r"series", SessionSeriesViewSet)
router.register(r"occurrences", SessionOccurrenceViewSet)
router.register(r"venues", VenueViewSet)

app_name = "sessions"

urlpatterns = [
    path("", include(router.urls)),
]
