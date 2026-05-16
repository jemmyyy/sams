from apps.academies.models import Academy
from apps.cancellations.models import CancellationPolicy, CancellationRequest
from apps.players.models import Player
from apps.sessions.models import SessionOccurrence, SessionSeries, Venue
from django.test import TestCase
from django.utils import timezone


class TestCancellationPolicyModel(TestCase):
    def setUp(self):
        self.academy = Academy.objects.create(name="Test Academy")

    def test_default_minimum_notice_hours_is_24(self):
        policy = CancellationPolicy.objects.create(academy=self.academy)
        assert policy.minimum_notice_hours == 24

    def test_default_auto_approve_enabled(self):
        policy = CancellationPolicy.objects.create(academy=self.academy)
        assert policy.auto_approve_enabled is True

    def test_default_refund_percentage_is_zero(self):
        policy = CancellationPolicy.objects.create(academy=self.academy)
        assert policy.refund_percentage == 0

    def test_default_is_active(self):
        policy = CancellationPolicy.objects.create(academy=self.academy)
        assert policy.is_active is True

    def test_str_representation(self):
        policy = CancellationPolicy.objects.create(academy=self.academy)
        assert str(policy) == f"Cancellation Policy — {self.academy.name}"


class TestCancellationPolicyAutoApproval(TestCase):
    def setUp(self):
        self.academy = Academy.objects.create(name="Test Academy")
        self.venue = Venue.objects.create(
            academy=self.academy, name="Test Venue", capacity=50
        )
        self.series = SessionSeries.objects.create(
            academy=self.academy,
            title="Test Series",
            start_date=timezone.now().date(),
            start_time="09:00:00",
            end_time="10:30:00",
            recurrence_rule="FREQ=WEEKLY;BYDAY=MO",
            venue=self.venue,
            max_capacity=20,
        )
        self.player = Player.objects.create(
            academy=self.academy,
            first_name="Test",
            last_name="Player",
            birth_date="2010-01-01",
            registration_number="REG001",
        )

    def _create_occurrence(self, hours_from_now):
        dt = timezone.now() + timezone.timedelta(hours=hours_from_now)
        return SessionOccurrence.objects.create(
            academy=self.academy,
            series=self.series,
            start_datetime=dt,
            end_datetime=dt + timezone.timedelta(hours=1.5),
            venue=self.venue,
            max_capacity=20,
        )

    def test_auto_approve_within_minimum_notice_window(self):
        policy = CancellationPolicy.objects.create(
            academy=self.academy,
            minimum_notice_hours=4,
            auto_approve_enabled=True,
            auto_approve_max_hours=48,
        )
        # Session is 2 hours from now — earlier than 4h minimum
        occurrence = self._create_occurrence(hours_from_now=2)
        request = CancellationRequest(
            occurrence=occurrence, player=self.player, academy=self.academy, reason="test"
        )
        ok, msg = policy.evaluate_auto_approval(request)
        assert ok is False
        assert "minimum notice" in msg.lower()

    def test_auto_approve_outside_auto_approve_window(self):
        policy = CancellationPolicy.objects.create(
            academy=self.academy,
            minimum_notice_hours=4,
            auto_approve_enabled=True,
            auto_approve_max_hours=48,
        )
        # Session is 96 hours from now — outside 48h auto-approve window
        occurrence = self._create_occurrence(hours_from_now=96)
        request = CancellationRequest(
            occurrence=occurrence, player=self.player, academy=self.academy, reason="test"
        )
        ok, msg = policy.evaluate_auto_approval(request)
        assert ok is False
        assert "auto-approve" in msg.lower()

    def test_auto_approve_within_window(self):
        policy = CancellationPolicy.objects.create(
            academy=self.academy,
            minimum_notice_hours=4,
            auto_approve_enabled=True,
            auto_approve_max_hours=48,
        )
        # Session is 12 hours from now — within notice AND within auto-approve window
        occurrence = self._create_occurrence(hours_from_now=12)
        request = CancellationRequest(
            occurrence=occurrence, player=self.player, academy=self.academy, reason="test"
        )
        ok, msg = policy.evaluate_auto_approval(request)
        assert ok is True

    def test_auto_approve_disabled_always_returns_pending(self):
        policy = CancellationPolicy.objects.create(
            academy=self.academy,
            minimum_notice_hours=4,
            auto_approve_enabled=False,
        )
        occurrence = self._create_occurrence(hours_from_now=12)
        request = CancellationRequest(
            occurrence=occurrence, player=self.player, academy=self.academy, reason="test"
        )
        ok, msg = policy.evaluate_auto_approval(request)
        assert ok is False
        assert "disabled" in msg.lower()
