from django.contrib import admin
from .models import NotificationTemplate, NotificationLog, UserNotificationPreference


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "is_active", "created_at")
    search_fields = ("name", "code")
    list_filter = ("is_active",)


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ("user", "channel", "status", "created_at")
    list_filter = ("channel", "status", "academy")
    search_fields = ("user__email", "user__username", "subject")
    readonly_fields = ("created_at", "updated_at")


@admin.register(UserNotificationPreference)
class UserNotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ("user", "channel", "is_enabled")
    list_filter = ("channel", "is_enabled")
    search_fields = ("user__email", "user__username")
