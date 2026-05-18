from datetime import time

from apps.academies.models import Academy
from apps.accounts.models import User
from apps.attendance.models import Attendance
from apps.common.thread_local import set_current_academy_id
from apps.players.models import Player
from apps.sessions.models import SessionSeries, SessionOccurrence, Venue
from django.test import TestCase
from django.utils import timezone


class TestAttendanceModel(TestCase):
    def setUp(self):
        self.academy = Academy.objects.create(name="Test Academy")
        set_current_academy_id(str(self.academy.id))
        self.user = User.objects.create_user(
            username="staff1", email="staff1@test.com", password="testpass123"
        )
        self.player = Player.objects.create(
            academy=self.academy,
            first_name="Test",
            last_name="Player",
            birth_date="2010-01-01",
            registration_number="REG001",
        )
        self.venue = Venue.objects.create(
            academy=self.academy,
            name="Main Field",
            capacity=50,
        )
        self.series = SessionSeries.objects.create(
            academy=self.academy,
            title="Test Series",
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=30),
            start_time=time(9, 0),
            end_time=time(10, 0),
            recurrence_rule="FREQ=WEEKLY;BYDAY=MO",
            venue=self.venue,
            max_capacity=30,
        )
        self.occurrence = SessionOccurrence.objects.create(
            academy=self.academy,
            series=self.series,
            start_datetime=timezone.now(),
            end_datetime=timezone.now() + timezone.timedelta(hours=1),
            venue=self.venue,
            max_capacity=30,
        )

    def tearDown(self):
        set_current_academy_id(None)

    def test_create_attendance_present(self):
        att = Attendance.objects.create(
            academy=self.academy,
            occurrence=self.occurrence,
            player=self.player,
            status="present",
            marked_by=self.user,
        )
        assert att.status == "present"
        assert att.marked_by == self.user

    def test_create_attendance_absent(self):
        att = Attendance.objects.create(
            academy=self.academy,
            occurrence=self.occurrence,
            player=self.player,
            status="absent",
            marked_by=self.user,
        )
        assert att.status == "absent"

    def test_attendance_str(self):
        att = Attendance.objects.create(
            academy=self.academy,
            occurrence=self.occurrence,
            player=self.player,
            status="present",
            marked_by=self.user,
        )
        assert "Test Player" in str(att)
