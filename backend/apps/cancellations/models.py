from apps.common.models import TenantAwareModel
from django.db import models
from django.utils import timezone


class CancellationPolicy(TenantAwareModel):
    minimum_notice_hours = models.PositiveIntegerField(default=24)
    auto_approve_enabled = models.BooleanField(default=True)
    auto_approve_max_hours = models.PositiveIntegerField(default=48)
    refund_percentage = models.PositiveSmallIntegerField(default=0)
    allow_coach_override = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Cancellation policies"

    def __str__(self):
        return f"Cancellation Policy — {self.academy.name}"

    def evaluate_auto_approval(self, cancellation_request):
        if not self.auto_approve_enabled:
            return False, "Auto-approval is disabled."

        hours_until_session = (
            cancellation_request.occurrence.start_datetime - timezone.now()
        ).total_seconds() / 3600

        if hours_until_session < self.minimum_notice_hours:
            return False, "Request is below minimum notice hours."

        if hours_until_session > self.auto_approve_max_hours:
            return False, "Request is outside auto-approve window."

        return True, "Auto-approved."


class CancellationRequest(TenantAwareModel):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    occurrence = models.ForeignKey(
        "academy_sessions.SessionOccurrence",
        on_delete=models.CASCADE,
        related_name="cancellation_requests",
    )
    player = models.ForeignKey(
        "players.Player", on_delete=models.CASCADE, related_name="cancellation_requests"
    )
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    request_date = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_cancellations",
    )
    review_notes = models.TextField(blank=True)

    def __str__(self):
        return f"Cancel Request: {self.player} for {self.occurrence}"
