from django.db import models
from apps.common.models import TenantAwareModel

class Venue(TenantAwareModel):
    name = models.CharField(max_length=255)
    location = models.TextField(blank=True)
    capacity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.academy.name})"

class SessionSeries(TenantAwareModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    # RFC5545 recurrence rule (e.g. "FREQ=WEEKLY;BYDAY=MO,WE")
    recurrence_rule = models.CharField(max_length=255)
    
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT, related_name='session_series')
    max_capacity = models.PositiveIntegerField()
    
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class SessionOccurrence(TenantAwareModel):
    series = models.ForeignKey(SessionSeries, on_delete=models.CASCADE, related_name='occurrences')
    start_datetime = models.DateTimeField(db_index=True)
    end_datetime = models.DateTimeField(db_index=True)
    
    # Overrides from series
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT, related_name='occurrences')
    max_capacity = models.PositiveIntegerField()
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('scheduled', 'Scheduled'),
            ('cancelled', 'Cancelled'),
            ('completed', 'Completed'),
        ],
        default='scheduled'
    )
    cancellation_reason = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['start_datetime', 'end_datetime']),
        ]

    def __str__(self):
        return f"{self.series.title} @ {self.start_datetime}"

class SessionCoach(TenantAwareModel):
    session = models.ForeignKey(SessionOccurrence, on_delete=models.CASCADE, related_name='coaches')
    coach = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='coaching_sessions')
    is_lead = models.BooleanField(default=False)

    class Meta:
        unique_together = ('session', 'coach')

class Enrollment(TenantAwareModel):
    session = models.ForeignKey(SessionOccurrence, on_delete=models.CASCADE, related_name='enrollments')
    player = models.ForeignKey('players.Player', on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('cancelled', 'Cancelled'),
            ('attended', 'Attended'),
            ('missed', 'Missed'),
        ],
        default='active'
    )

    class Meta:
        unique_together = ('session', 'player')

class ScheduleConflict(TenantAwareModel):
    occurrence = models.ForeignKey(SessionOccurrence, on_delete=models.CASCADE, related_name='conflicts')
    conflict_type = models.CharField(
        max_length=50,
        choices=[
            ('venue_double_booking', 'Venue Double Booking'),
            ('coach_overlap', 'Coach Overlap'),
        ]
    )
    description = models.TextField()
    resolved = models.BooleanField(default=False)
