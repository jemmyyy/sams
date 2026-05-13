from apps.common.models import TenantAwareModel
from django.db import models


class CancellationRequest(TenantAwareModel):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    occurrence = models.ForeignKey(
        "training_sessions.SessionOccurrence",
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
