import logging
from celery import shared_task
from django.utils import timezone
from apps.notifications.models import NotificationLog, NotificationStatus, ChannelChoices
from apps.notifications.services.adapters import (
    EmailAdapter, SMSAdapter, WhatsAppAdapter, PushAdapter, InAppAdapter
)

logger = logging.getLogger(__name__)

ADAPTER_MAP = {
    ChannelChoices.EMAIL: EmailAdapter,
    ChannelChoices.SMS: SMSAdapter,
    ChannelChoices.WHATSAPP: WhatsAppAdapter,
    ChannelChoices.PUSH: PushAdapter,
    ChannelChoices.IN_APP: InAppAdapter,
}

@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={'max_retries': 3},
    name="apps.notifications.tasks.send_notification_task"
)
def send_notification_task(self, log_id):
    """
    Celery task to send a notification using the appropriate adapter.
    """
    try:
        log = NotificationLog.all_objects.select_related('user', 'template').get(id=log_id)
    except NotificationLog.DoesNotExist:
        logger.error(f"NotificationLog {log_id} not found")
        return

    if log.status in [NotificationStatus.SENT, NotificationStatus.DELIVERED]:
        return

    adapter_class = ADAPTER_MAP.get(log.channel)
    if not adapter_class:
        log.status = NotificationStatus.FAILED
        log.error_message = f"No adapter found for channel {log.channel}"
        log.save()
        return

    adapter = adapter_class()
    success, error = adapter.send(
        recipient=log.user,
        subject=log.subject,
        content=log.content,
        metadata=log.metadata
    )

    if success:
        log.status = NotificationStatus.SENT
        log.sent_at = timezone.now()
        log.error_message = None
    else:
        log.status = NotificationStatus.FAILED
        log.error_message = error
        # If max retries reached, we just leave it as FAILED
        # Celery handles the retry logic itself

    log.save()


@shared_task(name="apps.notifications.tasks.dispatch_scheduled_notifications")
def dispatch_scheduled_notifications():
    ready = NotificationLog.all_objects.filter(
        status=NotificationStatus.PENDING,
        scheduled_at__lte=timezone.now(),
    )
    for log_entry in ready:
        send_notification_task.apply(args=[str(log_entry.id)])
