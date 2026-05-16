from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("id", "actor", "action", "entity_type", "entity_id", "academy", "created_at")
    list_filter = ("action", "entity_type", "academy", "created_at")
    search_fields = ("actor__username", "entity_type", "entity_id", "ip_address")
    readonly_fields = ("actor", "action", "entity_type", "entity_id", "old_value", "new_value", "ip_address", "user_agent", "metadata", "academy", "created_at")
    date_hierarchy = "created_at"
