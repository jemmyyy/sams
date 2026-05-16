from apps.permissions.permissions import IsCoach, IsCustomer, IsOperations
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Enrollment, SessionCoach, SessionOccurrence, SessionSeries, Venue
from ..serializers.session import (
    EnrollmentSerializer,
    SessionCoachSerializer,
    SessionOccurrenceSerializer,
    SessionSeriesSerializer,
    VenueSerializer,
)
from ..services.scheduling import SchedulingService


class SessionSeriesViewSet(viewsets.ModelViewSet):
    queryset = SessionSeries.objects.all()
    serializer_class = SessionSeriesSerializer
    permission_classes = [IsOperations]

    def perform_create(self, serializer):
        series = serializer.save()
        SchedulingService.generate_occurrences(series)


class SessionOccurrenceViewSet(viewsets.ModelViewSet):
    queryset = SessionOccurrence.objects.all()
    serializer_class = SessionOccurrenceSerializer
    permission_classes = [IsCoach]

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        occurrence = self.get_object()
        occurrence.status = "cancelled"
        occurrence.cancellation_reason = request.data.get("reason", "")
        occurrence.save()
        return Response({"status": "occurrence cancelled"})

    @action(detail=True, methods=["post"])
    def enroll(self, request, pk=None):
        occurrence = self.get_object()
        player_id = request.data.get("player_id")
        if not player_id:
            return Response({"error": "player_id required"}, status=status.HTTP_400_BAD_REQUEST)
        from apps.players.models import Player
        player = Player.objects.get(id=player_id)
        try:
            enrollment = SchedulingService.enroll_player(
                occurrence, player, occurrence.academy
            )
            return Response(EnrollmentSerializer(enrollment).data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def assign_coach(self, request, pk=None):
        occurrence = self.get_object()
        coach_id = request.data.get("coach_id")
        is_lead = request.data.get("is_lead", False)
        if not coach_id:
            return Response({"error": "coach_id required"}, status=status.HTTP_400_BAD_REQUEST)
        from django.contrib.auth import get_user_model
        User = get_user_model()
        coach = User.objects.get(id=coach_id)
        sc = SchedulingService.assign_coach(occurrence, coach, occurrence.academy, is_lead=is_lead)
        return Response(SessionCoachSerializer(sc).data, status=status.HTTP_201_CREATED)


class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [IsOperations]


class SessionCoachViewSet(viewsets.ModelViewSet):
    queryset = SessionCoach.objects.all()
    serializer_class = SessionCoachSerializer
    permission_classes = [IsOperations]


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsCustomer]
