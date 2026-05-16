from apps.common.models import TenantAwareModel
from django.db import models


class Coach(TenantAwareModel):
    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="coach_profiles"
    )
    specializations = models.JSONField(default=list, blank=True)
    certifications = models.JSONField(default=list, blank=True)
    bio = models.TextField(blank=True)
    hire_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    max_weekly_hours = models.PositiveIntegerField(default=40)

    class Meta:
        unique_together = ("user", "academy")

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} — Coach @ {self.academy.name}"


class CoachAvailability(TenantAwareModel):
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name="availabilities")
    day_of_week = models.PositiveSmallIntegerField(
        choices=[
            (0, "Monday"),
            (1, "Tuesday"),
            (2, "Wednesday"),
            (3, "Thursday"),
            (4, "Friday"),
            (5, "Saturday"),
            (6, "Sunday"),
        ]
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("coach", "day_of_week", "start_time")

    def __str__(self):
        return f"{self.coach} — {self.get_day_of_week_display()} {self.start_time}-{self.end_time}"
