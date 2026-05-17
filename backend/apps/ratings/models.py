from apps.common.models import TenantAwareModel
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class PlayerRating(TenantAwareModel):
    occurrence = models.ForeignKey(
        "academy_sessions.SessionOccurrence",
        on_delete=models.CASCADE,
        related_name="player_ratings",
    )
    player = models.ForeignKey("players.Player", on_delete=models.CASCADE, related_name="ratings")
    coach = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="given_ratings"
    )

    # Granular skill ratings (1-10 scale)
    technique = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    stamina = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    teamwork = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    behavior = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    performance_notes = models.TextField(blank=True)
    is_visible_to_parent = models.BooleanField(default=True)

    class Meta:
        unique_together = ("occurrence", "player", "coach")

    def __str__(self):
        return f"Rating: {self.player} by {self.coach} on {self.occurrence}"
