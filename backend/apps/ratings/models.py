from django.db import models
from apps.common.models import TenantAwareModel

class PlayerRating(TenantAwareModel):
    occurrence = models.ForeignKey(
        'sessions.SessionOccurrence',
        on_delete=models.CASCADE,
        related_name='player_ratings'
    )
    player = models.ForeignKey(
        'players.Player',
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    coach = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='given_ratings'
    )
    
    # Granular skill ratings
    technique = models.PositiveSmallIntegerField(default=0) # 1-10
    stamina = models.PositiveSmallIntegerField(default=0)
    teamwork = models.PositiveSmallIntegerField(default=0)
    behavior = models.PositiveSmallIntegerField(default=0)
    
    performance_notes = models.TextField(blank=True)
    is_visible_to_parent = models.BooleanField(default=True)

    class Meta:
        unique_together = ('occurrence', 'player', 'coach')

    def __str__(self):
        return f"Rating: {self.player} by {self.coach} on {self.occurrence}"
