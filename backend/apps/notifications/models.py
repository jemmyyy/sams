from django.db import models
from apps.common.models import UUIDModel, TimeStampedModel, TenantAwareModel
from django.utils.translation import gettext_lazy as _


class ChannelChoices(models.TextChoices):
    EMAIL = "email", _("Email")
    SMS = "sms", _("SMS")
    WHATSAPP = "whatsapp", _("WhatsApp")
    PUSH = "push", _("Push")
    IN_APP = "in_app", _("In-App")


class NotificationStatus(models.TextChoices):
    PENDING = "pending", _("Pending")
    SENT = "sent", _("Sent")
    DELIVERED = "delivered", _("Delivered")
    FAILED = "failed", _("Failed")


class NotificationTemplate(UUIDModel, TimeStampedModel):
    code = models.SlugField(unique=True, help_text=_("Unique identifier for the notification type (e.g. PAYMENT_SUCCESS)"))
    name = models.CharField(max_length=255)
    
    # Localized Content
    subject_en = models.CharField(max_length=255, blank=True)
    subject_ar = models.CharField(max_length=255, blank=True)
    
    content_en = models.TextField()
    content_ar = models.TextField()
    
    channels = models.JSONField(default=list, help_text=_("List of channels to use for this template (e.g. ['email', 'whatsapp'])"))
    
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class NotificationLog(TenantAwareModel):
    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="notification_logs"
    )
    template = models.ForeignKey(
        NotificationTemplate, on_delete=models.SET_NULL, null=True, blank=True
    )
    channel = models.CharField(max_length=20, choices=ChannelChoices.choices)
    status = models.CharField(
        max_length=20, choices=NotificationStatus.choices, default=NotificationStatus.PENDING
    )
    
    subject = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    
    error_message = models.TextField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.channel} to {self.user.email} - {self.status}"


class UserNotificationPreference(UUIDModel, TimeStampedModel):
    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="notification_preferences"
    )
    channel = models.CharField(max_length=20, choices=ChannelChoices.choices)
    is_enabled = models.BooleanField(default=True)

    class Meta:
        unique_together = ("user", "channel")

    def __str__(self):
        return f"{self.user.email} - {self.channel}: {'Enabled' if self.is_enabled else 'Disabled'}"
