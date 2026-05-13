from datetime import datetime

from dateutil.rrule import rrulestr
from django.db import transaction
from django.utils import timezone

from ..models import ScheduleConflict, SessionOccurrence, SessionSeries


class SchedulingService:
    @staticmethod
    def generate_occurrences(series: SessionSeries):
        """
        Generates SessionOccurrence instances based on a series recurrence rule.
        """
        start_dt = datetime.combine(series.start_date, series.start_time)
        end_dt = datetime.combine(series.start_date, series.end_time)
        duration = end_dt - start_dt

        occurrences = []

        # Use rrulestr for RFC5545 strings
        rule = rrulestr(series.recurrence_rule, dtstart=start_dt)

        with transaction.atomic():
            for dt in rule:
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
        Checks for venue and coach conflicts.
        """
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

        # Coach conflicts would be checked similarly by joining on SessionCoach
