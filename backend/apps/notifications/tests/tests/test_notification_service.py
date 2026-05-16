import pytest
from unittest.mock import patch, MagicMock
from django.core.cache import cache
from apps.notifications.models import NotificationTemplate, NotificationLog, NotificationStatus, ChannelChoices
from apps.notifications.services.notification_service import NotificationService
from apps.accounts.models import User
from apps.academies.models import Academy

@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", email="test@example.com", password="password")

@pytest.fixture
def academy(db):
    return Academy.objects.create(name="Test Academy", slug="test-academy")

@pytest.fixture
def template(db):
    return NotificationTemplate.objects.create(
        code="WELCOME_MSG",
        name="Welcome Message",
        subject_en="Welcome {{ name }}",
        content_en="Hello {{ name }}, welcome to SAMS!",
        channels=["email", "in_app"]
    )

@pytest.mark.django_db
class TestNotificationService:
    @patch('apps.notifications.tasks.send_notification_task.delay')
    def test_send_notification_success(self, mock_delay, user, template, academy):
        # Set thread-local academy
        with patch('apps.notifications.services.notification_service.get_current_academy_id', return_value=str(academy.id)):
            success = NotificationService.send_notification(
                user=user,
                template_code="WELCOME_MSG",
                context_data={"name": "John"}
            )
            
            assert success is True
            assert NotificationLog.objects.count() == 2
            
            # Check logs
            email_log = NotificationLog.objects.get(channel=ChannelChoices.EMAIL)
            assert email_log.subject == "Welcome John"
            assert email_log.content == "Hello John, welcome to SAMS!"
            assert email_log.status == NotificationStatus.PENDING
            
            in_app_log = NotificationLog.objects.get(channel=ChannelChoices.IN_APP)
            assert in_app_log.status == NotificationStatus.PENDING
            
            # Check celery calls
            assert mock_delay.call_count == 2

    def test_send_notification_throttled(self, user, template):
        cache.clear()
        # First call
        success1 = NotificationService.send_notification(
            user=user,
            template_code="WELCOME_MSG",
            rate_limit_seconds=60
        )
        assert success1 is True
        
        # Second call (throttled)
        success2 = NotificationService.send_notification(
            user=user,
            template_code="WELCOME_MSG",
            rate_limit_seconds=60
        )
        assert success2 is False

    @patch('apps.notifications.tasks.send_notification_task.delay')
    def test_user_preference_opt_out(self, mock_delay, user, template):
        from apps.notifications.models import UserNotificationPreference
        
        # Opt-out of email
        UserNotificationPreference.objects.create(user=user, channel=ChannelChoices.EMAIL, is_enabled=False)
        
        NotificationService.send_notification(user=user, template_code="WELCOME_MSG")
        
        # Should only have 1 log (in_app)
        assert NotificationLog.objects.count() == 1
        assert NotificationLog.objects.filter(channel=ChannelChoices.IN_APP).exists()
        assert not NotificationLog.objects.filter(channel=ChannelChoices.EMAIL).exists()
        assert mock_delay.call_count == 1
