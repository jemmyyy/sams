from datetime import datetime

from dateutil.rrule import rrulestr
from django.db import models, transaction
from django.utils import timezone

from ..models import Enrollment, ScheduleConflict, SessionCoach, SessionOccurrence, SessionSeries

MAX_OCCURRENCES = 500


class SchedulingService:
    @staticmethod
    def generate_occurrences(series: SessionSeries):
        """
        Generates SessionOccurrence instances based on a series recurrence rule.
        """
        start_dt = datetime.combine(series.start_date, series.start_time)
        end_dt = datetime.combine(series.start_date, series.end_time)
        duration = end_dt - start_dt

        rule = rrulestr(series.recurrence_rule, dtstart=start_dt)

        with transaction.atomic():
            occurrences = []
            for i, dt in enumerate(rule):
                if i >= MAX_OCCURRENCES:
                    break
                if series.end_date and dt.date() > series.end_date:
                    break

                occurrence = SessionOccurrence(
                    series=series,
                    academy=series.academy,
                    start_datetime=timezone.make_aware(dt),
                    end_datetime=timezone.make_aware(dt + duration),
                    venue=series.venue,
                    max_capacity=series.max_capacity,
                )
                occurrences.append(occurrence)

            SessionOccurrence.objects.bulk_create(occurrences)

    @staticmethod
    def detect_conflicts(occurrence: SessionOccurrence):
        """
        Checks for venue, coach, and player conflicts for an occurrence.
        """
        conflicts = []

        # Venue conflict
        venue_conflict = (
            SessionOccurrence.objects.filter(
                venue=occurrence.venue,
                start_datetime__lt=occurrence.end_datetime,
                end_datetime__gt=occurrence.start_datetime,
                status="scheduled",
            )
            .exclude(id=occurrence.id)
            .exists()
        )

        if venue_conflict:
            ScheduleConflict.objects.create(
                occurrence=occurrence,
                academy=occurrence.academy,
                conflict_type="venue_double_booking",
                description=f"Venue {occurrence.venue.name} is double booked.",
            )

        # Coach conflict: coaches assigned to this occurrence overlap with their other sessions
        coach_ids = SessionCoach.objects.filter(
            session=occurrence
        ).values_list("coach_id", flat=True)

        if coach_ids:
            overlapping_coach_sessions = (
                SessionCoach.objects.filter(
                    coach_id__in=coach_ids,
                    session__start_datetime__lt=occurrence.end_datetime,
                    session__end_datetime__gt=occurrence.start_datetime,
                    session__status="scheduled",
                )
                .exclude(session_id=occurrence.id)
                .select_related("session")
            )
            for sc in overlapping_coach_sessions:
                ScheduleConflict.objects.get_or_create(
                    occurrence=occurrence,
                    conflict_type="coach_overlap",
                    related_occurrence=sc.session,
                    defaults={
                        "academy": occurrence.academy,
                        "description": (
                            f"Coach assigned to both sessions: "
                            f"{occurrence.start_datetime} and {sc.session.start_datetime}"
                        ),
                    },
                )

        # Player conflict: enrolled players who have overlapping sessions
        player_ids = Enrollment.objects.filter(
            session=occurrence
        ).values_list("player_id", flat=True)

        if player_ids:
            overlapping_player_sessions = (
                Enrollment.objects.filter(
                    player_id__in=player_ids,
                    session__start_datetime__lt=occurrence.end_datetime,
                    session__end_datetime__gt=occurrence.start_datetime,
                    session__status="scheduled",
                )
                .exclude(session_id=occurrence.id)
                .select_related("session")
            )
            for enr in overlapping_player_sessions:
                ScheduleConflict.objects.get_or_create(
                    occurrence=occurrence,
                    conflict_type="player_overlap",
                    related_occurrence=enr.session,
                    defaults={
                        "academy": occurrence.academy,
                        "description": (
                            f"Player enrolled in both sessions: "
                            f"{occurrence.start_datetime} and {enr.session.start_datetime}"
                        ),
                    },
                )

        return conflicts

    @staticmethod
    def override_occurrence(occurrence: SessionOccurrence, **kwargs):
        """
        Override a single occurrence's properties (venue, time, capacity) independently
        of the series. Creates a conflict check after update.
        """
        allowed_fields = {"venue", "start_datetime", "end_datetime", "max_capacity", "notes"}
        changed = False
        for field, value in kwargs.items():
            if field in allowed_fields and hasattr(occurrence, field):
                setattr(occurrence, field, value)
                changed = True

        if changed:
            occurrence.save()
            SchedulingService.detect_conflicts(occurrence)

        return occurrence

    @staticmethod
    def check_capacity(occurrence: SessionOccurrence):
        """
        Returns (is_full, current_count, max_capacity).
        """
        count = Enrollment.objects.filter(session=occurrence).count()
        return count >= occurrence.max_capacity, count, occurrence.max_capacity

    @staticmethod
    def enroll_player(occurrence: SessionOccurrence, player, academy):
        """
        Enrolls a player in an occurrence, checking capacity first.
        Raises ValueError if session is full.
        """
        is_full, count, max_cap = SchedulingService.check_capacity(occurrence)
        if is_full:
            raise ValueError(
                f"Session is full ({count}/{max_cap} enrolled)"
            )

        enrollment, created = Enrollment.objects.get_or_create(
            session=occurrence,
            player=player,
            defaults={"academy": academy, "status": "active"},
        )
        if not created:
            enrollment.status = "active"
            enrollment.save()

        SchedulingService.detect_conflicts(occurrence)
        return enrollment

    @staticmethod
    def assign_coach(occurrence: SessionOccurrence, coach, academy, is_lead=False):
        """
        Assigns a coach to an occurrence, then checks for conflicts.
        """
        sc, created = SessionCoach.objects.get_or_create(
            session=occurrence,
            coach=coach,
            defaults={"academy": academy, "is_lead": is_lead},
        )
        if not created and is_lead:
            sc.is_lead = True
            sc.save()

        SchedulingService.detect_conflicts(occurrence)
        return sc
