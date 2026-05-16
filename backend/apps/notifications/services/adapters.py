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


class SMSAdapter(BaseChannelAdapter):
    def send(self, recipient, subject, content, metadata=None):
        """Sends SMS via a configured provider (Twilio, etc.). Currently a stub awaiting provider integration."""
        phone = getattr(recipient, 'phone_number', None)
        if not phone:
            logger.warning(f"No phone number for user {recipient.id}")
            return False, "No phone number"
        logger.info(f"SMS to {phone}: {content[:70]}... [STUB - configure provider]")
        return True, None


class WhatsAppAdapter(BaseChannelAdapter):
    def send(self, recipient, subject, content, metadata=None):
        logger.info(f"WhatsApp to {recipient.phone_number}: {content[:50]}... [STUB]")
        return True, None


class PushAdapter(BaseChannelAdapter):
    def send(self, recipient, subject, content, metadata=None):
        logger.info(f"Push to {recipient.id}: {subject} [STUB]")
        return True, None


class InAppAdapter(BaseChannelAdapter):
    def send(self, recipient, subject, content, metadata=None):
        logger.info(f"In-App delivery for {recipient.id}")
        return True, None
