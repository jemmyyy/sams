import pytest
from unittest.mock import patch

from django.core.cache import cache

from apps.academies.models import Academy
from apps.accounts.models import User
from apps.common.thread_local import set_current_academy_id
from apps.notifications.models import (
    ChannelChoices,
    NotificationLog,
    NotificationStatus,
    NotificationTemplate,
    UserNotificationPreference,
)
from apps.notifications.services.notification_service import NotificationService


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", email="test@example.com", password="password")


@pytest.fixture
def academy(db):
    return Academy.objects.create(name="Test Academy", slug="test-academy")


@pytest.fixture(autouse=True)
def _set_academy(academy):
    set_current_academy_id(str(academy.id))
    yield
    set_current_academy_id(None)


@pytest.fixture
def template(db):
    return NotificationTemplate.objects.create(
        code="WELCOME_MSG",
        name="Welcome Message",
        subject_en="Welcome {{ name }}",
        content_en="Hello {{ name }}, welcome to SAMS!",
        channels=["email", "in_app"],
    )


@pytest.mark.django_db
class TestNotificationService:
    @patch("apps.notifications.tasks.send_notification_task.delay")
    def test_send_notification_success(self, mock_delay, user, template):
        success = NotificationService.send_notification(
            user=user,
            template_code="WELCOME_MSG",
            context_data={"name": "John"},
        )
        assert success is True
        assert NotificationLog.objects.count() == 2

        email_log = NotificationLog.objects.get(channel=ChannelChoices.EMAIL)
        assert email_log.subject == "Welcome John"
        assert email_log.content == "Hello John, welcome to SAMS!"
        assert email_log.status == NotificationStatus.PENDING

        in_app_log = NotificationLog.objects.get(channel=ChannelChoices.IN_APP)
        assert in_app_log.status == NotificationStatus.PENDING
        assert mock_delay.call_count == 2

    def test_send_notification_throttled(self, user, template):
        cache.clear()
        success1 = NotificationService.send_notification(
            user=user, template_code="WELCOME_MSG", rate_limit_seconds=60
        )
        assert success1 is True

        success2 = NotificationService.send_notification(
            user=user, template_code="WELCOME_MSG", rate_limit_seconds=60
        )
        assert success2 is False

    @patch("apps.notifications.tasks.send_notification_task.delay")
    def test_user_preference_opt_out(self, mock_delay, user, template):
        UserNotificationPreference.objects.create(
            user=user, channel=ChannelChoices.EMAIL, is_enabled=False
        )
        NotificationService.send_notification(user=user, template_code="WELCOME_MSG")

        assert NotificationLog.objects.count() == 1
        assert NotificationLog.objects.filter(channel=ChannelChoices.IN_APP).exists()
        assert not NotificationLog.objects.filter(channel=ChannelChoices.EMAIL).exists()
        assert mock_delay.call_count == 1
