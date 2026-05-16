import pytest
from unittest.mock import patch, MagicMock
from apps.notifications.models import NotificationLog, NotificationStatus, ChannelChoices
from apps.notifications.tasks import send_notification_task
from apps.accounts.models import User
from apps.academies.models import Academy

@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", email="test@example.com", password="password")

@pytest.fixture
def academy(db):
    return Academy.objects.create(name="Test Academy", slug="test-academy")

@pytest.mark.django_db
class TestNotificationTasks:
    @patch('apps.notifications.services.adapters.EmailAdapter.send')
    def test_send_notification_task_email_success(self, mock_send, user, academy):
        mock_send.return_value = (True, None)
        
        log = NotificationLog.objects.create(
            user=user,
            channel=ChannelChoices.EMAIL,
            subject="Test",
            content="Content",
            academy=academy
        )
        
        send_notification_task(str(log.id))
        
        log.refresh_from_db()
        assert log.status == NotificationStatus.SENT
        assert log.sent_at is not None
        assert log.error_message is None

    @patch('apps.notifications.services.adapters.EmailAdapter.send')
    def test_send_notification_task_email_failure(self, mock_send, user, academy):
        mock_send.return_value = (False, "Connection timeout")
        
        log = NotificationLog.objects.create(
            user=user,
            channel=ChannelChoices.EMAIL,
            subject="Test",
            content="Content",
            academy=academy
        )
        
        send_notification_task(str(log.id))
        
        log.refresh_from_db()
        assert log.status == NotificationStatus.FAILED
        assert log.error_message == "Connection timeout"
