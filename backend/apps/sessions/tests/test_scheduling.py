import pytest
from datetime import date, time, timedelta
from apps.academies.models import Academy
from apps.sessions.models import Venue, SessionSeries, SessionOccurrence
from apps.sessions.services.scheduling import SchedulingService

@pytest.fixture
def academy(db):
    return Academy.objects.create(name="Test Academy", slug="test-academy")

@pytest.fixture
def venue(academy):
    return Venue.objects.create(name="Court 1", capacity=10, academy=academy)

@pytest.mark.django_db
class TestSchedulingEngine:
    def test_generate_occurrences(self, academy, venue):
        series = SessionSeries.objects.create(
            academy=academy,
            title="Weekly Tennis",
            start_date=date(2026, 6, 1),
            end_date=date(2026, 6, 30),
            start_time=time(10, 0),
            end_time=time(11, 0),
            recurrence_rule="FREQ=WEEKLY;BYDAY=MO",
            venue=venue,
            max_capacity=10
        )
        
        SchedulingService.generate_occurrences(series)
        
        # June 2026 has 5 Mondays: 1, 8, 15, 22, 29
        assert SessionOccurrence.objects.filter(series=series).count() == 5
        
    def test_venue_conflict_detection(self, academy, venue):
        series = SessionSeries.objects.create(
            academy=academy,
            title="S1",
            start_date=date(2026, 6, 1),
            start_time=time(10, 0),
            end_time=time(11, 0),
            recurrence_rule="FREQ=ONCE",
            venue=venue,
            max_capacity=10
        )
        SchedulingService.generate_occurrences(series)
        occ1 = SessionOccurrence.objects.first()
        
        # Create a second session at the same time and venue
        series2 = SessionSeries.objects.create(
            academy=academy,
            title="S2",
            start_date=date(2026, 6, 1),
            start_time=time(10, 30),
            end_time=time(11, 30),
            recurrence_rule="FREQ=ONCE",
            venue=venue,
            max_capacity=10
        )
        SchedulingService.generate_occurrences(series2)
        occ2 = SessionOccurrence.objects.filter(series=series2).first()
        
        SchedulingService.detect_conflicts(occ2)
        assert occ2.conflicts.filter(conflict_type='venue_double_booking').exists()
