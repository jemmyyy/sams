from apps.common.models import TenantAwareModel
from django.db import models


class Group(TenantAwareModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    level = models.CharField(max_length=100, blank=True)  # e.g., Beginner, Advanced

    players = models.ManyToManyField("players.Player", related_name="player_groups", blank=True)

    # Groups can be assigned to session series or individual occurrences
    sessions = models.ManyToManyField(
        "academy_sessions.SessionSeries", related_name="groups", blank=True
    )

    def __str__(self):
        return f"{self.name} ({self.academy.name})"


class GroupCoach(TenantAwareModel):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="coaches")
    coach = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="assigned_groups"
    )
    is_lead = models.BooleanField(default=False)

    class Meta:
        unique_together = ("group", "coach")
