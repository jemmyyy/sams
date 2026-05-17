from apps.common.models import TenantAwareModel
from django.db import models


class SessionReport(TenantAwareModel):
    occurrence = models.OneToOneField(
        "academy_sessions.SessionOccurrence", on_delete=models.CASCADE, related_name="report"
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

class GeneratedReport(TenantAwareModel):
    REPORT_TYPES = [
        ("financial", "Financial Report"),
        ("attendance", "Attendance Report"),
        ("utilization", "Utilization Report"),
        ("performance", "Performance Report"),
    ]
    
    FORMAT_CHOICES = [
        ("pdf", "PDF"),
        ("xlsx", "Excel"),
        ("csv", "CSV"),
    ]
    
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    
    file = models.FileField(upload_to="reports/%Y/%m/%d/", null=True, blank=True)
    error_message = models.TextField(blank=True)
    
    parameters = models.JSONField(default=dict, blank=True)
    
    requested_by = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"{self.report_type} ({self.format}) - {self.status}"

class ScheduledReport(TenantAwareModel):
    FREQUENCY_CHOICES = [
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
    ]

    name = models.CharField(max_length=255)
    report_type = models.CharField(max_length=50, choices=GeneratedReport.REPORT_TYPES)
    format = models.CharField(max_length=10, choices=GeneratedReport.FORMAT_CHOICES)
    
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    recipients = models.JSONField(default=list, help_text="List of email addresses")
    
    is_active = models.BooleanField(default=True)
    last_run_at = models.DateTimeField(null=True, blank=True)
    
    parameters = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.name} ({self.frequency})"
