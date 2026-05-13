from apps.common.models import TenantAwareModel
from django.db import models


class SessionReport(TenantAwareModel):
    occurrence = models.OneToOneField(
        "training_sessions.SessionOccurrence", on_delete=models.CASCADE, related_name="report"
    )
    coach = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="session_reports"
    )
    summary = models.TextField()
    achievements = models.TextField(blank=True)
    challenges = models.TextField(blank=True)
    next_steps = models.TextField(blank=True)

    submitted_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Report for {self.occurrence}"
