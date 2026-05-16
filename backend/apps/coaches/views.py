from apps.common.thread_local import get_current_academy_id
from apps.permissions.permissions import IsCoach, IsOperations
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Coach, CoachAvailability
from .serializers import CoachAvailabilitySerializer, CoachSerializer


class CoachViewSet(viewsets.ModelViewSet):
    queryset = Coach.objects.select_related("user").all()
    serializer_class = CoachSerializer
    permission_classes = [IsOperations]
    search_fields = ["user__first_name", "user__last_name", "user__email", "specializations"]
    filterset_fields = ["is_active"]

    def get_queryset(self):
        qs = super().get_queryset()
        include_inactive = self.request.query_params.get("include_inactive", "false").lower() == "true"
        if not include_inactive:
            qs = qs.filter(is_active=True)
        return qs

    @action(detail=True, methods=["get"], url_path="workload")
    def workload(self, request, pk=None):
        coach = self.get_object()
        from apps.sessions.models import SessionCoach

        upcoming = (
            SessionCoach.objects.filter(coach=coach.user, session__start_datetime__gte=timezone.now())
            .select_related("session")
            .count()
        )
        total_hours = (
            SessionCoach.objects.filter(
                coach=coach.user,
                session__start_datetime__gte=timezone.now(),
            ).count()
            * 1.5  # rough estimate: avg session 1.5 hours
        )
        return Response(
            {
                "coach_id": str(coach.id),
                "user_name": coach.user.get_full_name() or coach.user.username,
                "max_weekly_hours": coach.max_weekly_hours,
                "upcoming_sessions": upcoming,
                "estimated_weekly_hours": round(total_hours, 1),
            }
        )

    @action(detail=True, methods=["post"], url_path="toggle-active")
    def toggle_active(self, request, pk=None):
        coach = self.get_object()
        coach.is_active = not coach.is_active
        coach.save(update_fields=["is_active"])
        return Response({"is_active": coach.is_active})


class CoachAvailabilityViewSet(viewsets.ModelViewSet):
    serializer_class = CoachAvailabilitySerializer
    permission_classes = [IsCoach]

    def get_queryset(self):
        academy_id = get_current_academy_id()
        return CoachAvailability.objects.filter(
            academy_id=academy_id, coach_id=self.kwargs.get("coach_pk")
        ).select_related("coach")

    def perform_create(self, serializer):
        coach = Coach.objects.get(pk=self.kwargs["coach_pk"])
        serializer.save(coach=coach)
