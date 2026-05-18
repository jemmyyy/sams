from apps.academies.models import Academy
from apps.accounts.models import User
from apps.coaches.models import Coach, CoachAvailability
from apps.common.thread_local import set_current_academy_id
from django.test import TestCase


class TestCoachModel(TestCase):
    def setUp(self):
        self.academy = Academy.objects.create(name="Test Academy")
        set_current_academy_id(str(self.academy.id))
        self.user = User.objects.create_user(
            username="coach1", email="coach1@test.com", password="testpass123"
        )
        self.coach = Coach.objects.create(
            academy=self.academy,
            user=self.user,
            bio="Experienced coach",
            max_weekly_hours=35,
        )

    def tearDown(self):
        set_current_academy_id(None)

    def test_coach_creation(self):
        assert self.coach.is_active is True
        assert self.coach.max_weekly_hours == 35
        assert self.coach.bio == "Experienced coach"

    def test_coach_str(self):
        assert "coach1" in str(self.coach) or "Coach" in str(self.coach)

    def test_coach_unique_per_academy(self):
        from django.db import IntegrityError

        with self.assertRaises(IntegrityError):
            Coach.objects.create(
                academy=self.academy,
                user=self.user,
            )


class TestCoachAvailability(TestCase):
    def setUp(self):
        self.academy = Academy.objects.create(name="Test Academy")
        set_current_academy_id(str(self.academy.id))
        self.user = User.objects.create_user(
            username="coach2", email="coach2@test.com", password="testpass123"
        )
        self.coach = Coach.objects.create(
            academy=self.academy, user=self.user
        )

    def tearDown(self):
        set_current_academy_id(None)

    def test_create_availability(self):
        avail = CoachAvailability.objects.create(
            academy=self.academy,
            coach=self.coach,
            day_of_week=1,
            start_time="09:00",
            end_time="12:00",
        )
        assert avail.day_of_week == 1

    def test_multiple_availabilities(self):
        CoachAvailability.objects.create(
            academy=self.academy, coach=self.coach,
            day_of_week=1, start_time="09:00", end_time="12:00",
        )
        CoachAvailability.objects.create(
            academy=self.academy, coach=self.coach,
            day_of_week=3, start_time="14:00", end_time="17:00",
        )
        count = CoachAvailability.objects.filter(coach=self.coach).count()
        assert count == 2
