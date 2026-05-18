import logging
from django.template import Template, Context
from django.utils import timezone
from apps.notifications.models import (
    NotificationTemplate, 
    NotificationLog, 
    UserNotificationPreference,
    ChannelChoices,
    NotificationStatus
)
from apps.common.thread_local import get_current_academy_id
from django.core.cache import cache

logger = logging.getLogger(__name__)

class NotificationService:
    @staticmethod
    def _check_throttle(user, template_code, rate_limit_seconds=60):
        """
        Prevents sending the same notification to the same user within a short timeframe.
        Returns True if throttled, False otherwise.
        """
        cache_key = f"throttle:notify:{user.id}:{template_code}"
        if cache.get(cache_key):
            return True
        
        cache.set(cache_key, True, rate_limit_seconds)
        return False

    @staticmethod
    def send_notification(user, template_code, context_data=None, academy_id=None, rate_limit_seconds=None):
        """
        Main entry point for sending notifications.
        Queues async tasks for each configured channel.
        """
        if rate_limit_seconds and NotificationService._check_throttle(user, template_code, rate_limit_seconds):
            logger.warning(f"Notification throttled for user {user.id} and template {template_code}")
            return False

        context_data = context_data or {}
        academy_id = academy_id or get_current_academy_id()
        
        try:
            template = NotificationTemplate.objects.get(code=template_code, is_active=True)
        except NotificationTemplate.DoesNotExist:
            logger.error(f"Notification template not found or inactive: {template_code}")
            return False

        # 1. Determine which channels to use
        # Intersection of template channels and user preferences
        channels = template.channels
        user_prefs = UserNotificationPreference.objects.filter(user=user).values_list('channel', 'is_enabled')
        prefs_dict = {c: enabled for c, enabled in user_prefs}
        
        active_channels = []
        for channel in channels:
            # Default to enabled if no preference set
            if prefs_dict.get(channel, True):
                active_channels.append(channel)

        if not active_channels:
            logger.info(f"No active channels for user {user.id} and template {template_code}")
            return True

        # 2. Render content (localized)
        # Assuming user language preference exists or default to 'en'
        lang = getattr(user, 'preferred_language', 'en') # Need to verify if User has this field
        
        subject_template = getattr(template, f'subject_{lang}', template.subject_en)
        content_template = getattr(template, f'content_{lang}', template.content_en)
        
        subject = Template(subject_template).render(Context(context_data))
        content = Template(content_template).render(Context(context_data))

        # 3. Create logs and queue tasks
        # We import tasks inside the method to avoid circular imports if any
        from apps.notifications.tasks import send_notification_task
        
        for channel in active_channels:
            log = NotificationLog.objects.create(
                user=user,
                template=template,
                channel=channel,
                status=NotificationStatus.PENDING,
                subject=subject,
                content=content,
                academy_id=academy_id
            )
            
            # Queue the Celery task
            send_notification_task.delay(str(log.id))
            
        return True

    @staticmethod
    def broadcast_notification(users_queryset, template_code, context_data=None, academy_id=None):
        """
        Sends a notification to a queryset of users using bulk_create.
        """
        context_data = context_data or {}
        academy_id = academy_id or get_current_academy_id()

        try:
            template = NotificationTemplate.objects.get(code=template_code, is_active=True)
        except NotificationTemplate.DoesNotExist:
            logger.error(f"Notification template not found or inactive: {template_code}")
            return 0

        channels = template.channels

        lang = "en"
        subject = Template(getattr(template, f"subject_{lang}", template.subject_en)).render(Context(context_data))
        content = Template(getattr(template, f"content_{lang}", template.content_en)).render(Context(context_data))

        from apps.notifications.tasks import send_notification_task

        logs = []
        for user in users_queryset:
            if NotificationService._check_throttle(user, template_code, rate_limit_seconds=60):
                continue

            user_prefs = UserNotificationPreference.objects.filter(user=user).values_list("channel", "is_enabled")
            prefs_dict = {c: enabled for c, enabled in user_prefs}

            for channel in channels:
                if not prefs_dict.get(channel, True):
                    continue
                logs.append(NotificationLog(
                    user=user,
                    template=template,
                    channel=channel,
                    status=NotificationStatus.PENDING,
                    subject=subject,
                    content=content,
                    academy_id=academy_id,
                ))

        if logs:
            created_logs = NotificationLog.objects.bulk_create(logs)
            for log in created_logs:
                send_notification_task.delay(str(log.id))

        return len(logs)
