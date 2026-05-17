from apps.common.models import TenantAwareModel
from django.db import models


class Attendance(TenantAwareModel):
    STATUS_CHOICES = [
        ("present", "Present"),
        ("absent", "Absent"),
        ("late", "Late"),
        ("excused", "Excused"),
    ]

    occurrence = models.ForeignKey(
        "academy_sessions.SessionOccurrence",
        on_delete=models.CASCADE,
        related_name="attendance_records",
    )
    player = models.ForeignKey(
        "players.Player", on_delete=models.CASCADE, related_name="attendance_history"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    marked_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, related_name="marked_attendance"
    )
    timestamp = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ("occurrence", "player")

    def __str__(self):
        return f"{self.player} - {self.occurrence} - {self.status}"
