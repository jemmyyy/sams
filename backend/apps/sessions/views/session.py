from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import SessionOccurrence, SessionSeries, Venue
from ..serializers.session import (
    SessionOccurrenceSerializer,
    SessionSeriesSerializer,
    VenueSerializer,
)
from ..services.scheduling import SchedulingService


class SessionSeriesViewSet(viewsets.ModelViewSet):
    queryset = SessionSeries.objects.all()
    serializer_class = SessionSeriesSerializer

    def perform_create(self, serializer):
        series = serializer.save()
        SchedulingService.generate_occurrences(series)


class SessionOccurrenceViewSet(viewsets.ModelViewSet):
    queryset = SessionOccurrence.objects.all()
    serializer_class = SessionOccurrenceSerializer

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        occurrence = self.get_object()
        occurrence.status = "cancelled"
        occurrence.cancellation_reason = request.data.get("reason", "")
        occurrence.save()
        return Response({"status": "occurrence cancelled"})


class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
