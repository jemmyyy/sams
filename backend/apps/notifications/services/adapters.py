from abc import ABC, abstractmethod
import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

class BaseChannelAdapter(ABC):
    @abstractmethod
    def send(self, recipient, subject, content, metadata=None):
        pass


class EmailAdapter(BaseChannelAdapter):
    def send(self, recipient, subject, content, metadata=None):
        try:
            # For production, this would use a more robust backend or template-based email
            send_mail(
                subject=subject,
                message=content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient.email],
                fail_silently=False,
                html_message=content if "<html>" in content else None
            )
            return True, None
        except Exception as e:
            logger.error(f"Email failed to {recipient.email}: {str(e)}")
            return False, str(e)


class WhatsAppAdapter(BaseChannelAdapter):
    def send(self, recipient, subject, content, metadata=None):
        # MOCK Implementation
        logger.info(f"MOCK WhatsApp sent to {recipient.phone_number}: {content[:50]}...")
        return True, None


class PushAdapter(BaseChannelAdapter):
    def send(self, recipient, subject, content, metadata=None):
        # MOCK Implementation
        logger.info(f"MOCK Push sent to {recipient.id}: {subject}")
        return True, None


class InAppAdapter(BaseChannelAdapter):
    def send(self, recipient, subject, content, metadata=None):
        # In-app notifications are usually just DB records which we already create in the service
        # but this adapter could be used for real-time delivery via WebSockets/Centrifugo
        logger.info(f"MOCK In-App delivery for {recipient.id}")
        return True, None
