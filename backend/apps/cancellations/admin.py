from django.contrib import admin

from .models import CancellationPolicy, CancellationRequest


@admin.register(CancellationPolicy)
class CancellationPolicyAdmin(admin.ModelAdmin):
    list_display = ("id", "academy", "minimum_notice_hours", "auto_approve_enabled", "refund_percentage", "is_active")
    list_filter = ("is_active", "auto_approve_enabled")


@admin.register(CancellationRequest)
class CancellationRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "player", "occurrence", "status", "request_date")
    list_filter = ("status", "request_date")
    search_fields = ("player__first_name", "player__last_name", "reason")
