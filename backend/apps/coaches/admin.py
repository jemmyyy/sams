from django.contrib import admin

from .models import Coach, CoachAvailability


@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "academy", "is_active", "hire_date", "max_weekly_hours")
    list_filter = ("is_active", "academy")
    search_fields = ("user__first_name", "user__last_name", "user__email")


@admin.register(CoachAvailability)
class CoachAvailabilityAdmin(admin.ModelAdmin):
    list_display = ("id", "coach", "day_of_week", "start_time", "end_time", "is_active")
    list_filter = ("is_active", "day_of_week")
