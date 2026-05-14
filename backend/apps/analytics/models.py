from django.db import models
from apps.common.models import TenantAwareModel, UUIDModel, TimeStampedModel
from django.utils.translation import gettext_lazy as _

class DailyRevenueSnapshot(TenantAwareModel):
    date = models.DateField()
    total_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_refunds = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("academy", "date")
        ordering = ["-date"]

class DailyAttendanceSnapshot(TenantAwareModel):
    date = models.DateField()
    total_expected = models.PositiveIntegerField(default=0)
    total_present = models.PositiveIntegerField(default=0)
    total_absent = models.PositiveIntegerField(default=0)
    attendance_rate = models.FloatField(default=0) # Percentage

    class Meta:
        unique_together = ("academy", "date")
        ordering = ["-date"]

class MonthlyEnrollmentSnapshot(TenantAwareModel):
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    total_active_players = models.PositiveIntegerField(default=0)
    new_enrollments = models.PositiveIntegerField(default=0)
    churned_players = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("academy", "year", "month")
        ordering = ["-year", "-month"]

class CoachPerformanceSnapshot(TenantAwareModel):
    coach = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    period_start = models.DateField()
    period_end = models.DateField()
    sessions_conducted = models.PositiveIntegerField(default=0)
    average_attendance_rate = models.FloatField(default=0)
    reports_submitted = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("academy", "coach", "period_start", "period_end")
