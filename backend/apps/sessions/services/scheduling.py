from datetime import datetime, combine, timedelta
from dateutil.rrule import rrule, rruleset, str_to_iderive
from django.db import transaction
from django.utils import timezone
from ..models import SessionSeries, SessionOccurrence, ScheduleConflict

class SchedulingService:
    @staticmethod
    def generate_occurrences(series: SessionSeries):
        """
        Generates SessionOccurrence instances based on a series recurrence rule.
        """
        # Note: In a real enterprise app, we'd use a more robust RFC library 
        # like 'django-recurrence' or direct 'dateutil.rrule' parsing.
        # For brevity, we assume a standard rrule string.
        
        start_dt = combine(series.start_date, series.start_time)
        end_dt = combine(series.start_date, series.end_time)
        duration = end_dt - start_dt
        
        occurrences = []
        
        # rrule example: "FREQ=WEEKLY;UNTIL=20261231T235959Z"
        rule = rrule.from_text(series.recurrence_rule, dtstart=start_dt)
        
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
                    max_capacity=series.max_capacity
                )
                occurrences.append(occurrence)
            
            SessionOccurrence.objects.bulk_create(occurrences)
            
    @staticmethod
    def detect_conflicts(occurrence: SessionOccurrence):
        """
        Checks for venue and coach conflicts.
        """
        # Venue conflict
        venue_conflict = SessionOccurrence.objects.filter(
            venue=occurrence.venue,
            start_datetime__lt=occurrence.end_datetime,
            end_datetime__gt=occurrence.start_datetime,
            status='scheduled'
        ).exclude(id=occurrence.id).exists()
        
        if venue_conflict:
            ScheduleConflict.objects.create(
                occurrence=occurrence,
                academy=occurrence.academy,
                conflict_type='venue_double_booking',
                description=f"Venue {occurrence.venue.name} is double booked."
            )
            
        # Coach conflicts would be checked similarly by joining on SessionCoach
