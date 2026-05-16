from datetime import timedelta

from apps.academies.models import Academy
from apps.accounts.models import User
from apps.notifications.models import ChannelChoices, NotificationLog, NotificationStatus
from django.test import TestCase
from django.utils import timezone


class TestNotificationScheduling(TestCase):
    def setUp(self):
        self.academy = Academy.objects.create(name="Test Academy")
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_scheduled_at_default_is_none(self):
        log = NotificationLog.objects.create(
            academy=self.academy,
            user=self.user,
            channel=ChannelChoices.PUSH,
            content="Test notification",
        )
        assert log.scheduled_at is None

    def test_scheduled_notification_not_dispatched_before_scheduled_time(self):
        future = timezone.now() + timedelta(hours=2)
        log = NotificationLog.objects.create(
            academy=self.academy,
            user=self.user,
            channel=ChannelChoices.PUSH,
            content="Future notification",
            scheduled_at=future,
            status=NotificationStatus.PENDING,
        )
        ready = NotificationLog.all_objects.filter(
            status=NotificationStatus.PENDING,
            scheduled_at__lte=timezone.now(),
        )
        assert ready.count() == 0

    def test_scheduled_notification_dispatched_after_scheduled_time(self):
        past = timezone.now() - timedelta(hours=1)
        log = NotificationLog.objects.create(
            academy=self.academy,
            user=self.user,
            channel=ChannelChoices.PUSH,
            content="Past-due notification",
            scheduled_at=past,
            status=NotificationStatus.PENDING,
        )
        ready = NotificationLog.all_objects.filter(
            status=NotificationStatus.PENDING,
            scheduled_at__lte=timezone.now(),
        )
        assert ready.count() == 1
        assert ready.first().id == log.id

    def test_immediate_notification_has_no_scheduled_at(self):
        log = NotificationLog.objects.create(
            academy=self.academy,
            user=self.user,
            channel=ChannelChoices.PUSH,
            content="Immediate notification",
        )
        ready = NotificationLog.all_objects.filter(
            status=NotificationStatus.PENDING,
            scheduled_at__isnull=True,
        )
        assert ready.count() == 1

    def test_dispatch_scheduled_notifications_updates_status(self):
        from apps.notifications.tasks import dispatch_scheduled_notifications

        past = timezone.now() - timedelta(hours=1)
        log = NotificationLog.all_objects.create(
            academy=self.academy,
            user=self.user,
            channel=ChannelChoices.PUSH,
            content="Dispatch me",
            scheduled_at=past,
            status=NotificationStatus.PENDING,
        )
        dispatch_scheduled_notifications()
        log = NotificationLog.all_objects.get(pk=log.pk)
        assert log.status in [NotificationStatus.SENT, NotificationStatus.FAILED]
