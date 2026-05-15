from apps.common.models import TenantAwareModel
from django.db import models


class Announcement(TenantAwareModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    target_roles = models.JSONField(default=list)  # List of roles like ['coach', 'customer']
    created_by = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    is_published = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title


class NotificationLog(TenantAwareModel):
    academy = models.ForeignKey(
        "academies.Academy", on_delete=models.CASCADE, related_name="communication_logs"
    )
    announcement = models.ForeignKey(
        Announcement, on_delete=models.CASCADE, related_name="delivery_logs"
    )
    recipient = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
