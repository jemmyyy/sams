from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.analytics.tasks import (
    refresh_daily_revenue, 
    refresh_daily_attendance, 
    refresh_monthly_enrollment, 
    refresh_coach_performance
)

class Command(BaseCommand):
    help = "Build historical analytics snapshots"

    def add_arguments(self, parser):
        parser.add_argument("--days", type=int, default=30, help="Number of days to go back")

    def handle(self, *args, **options):
        days = options["days"]
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days)

        self.stdout.write(f"Building historical analytics from {start_date} to {end_date}...")

        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")
            self.stdout.write(f"Processing {date_str}...")
            
            refresh_daily_revenue.delay(date_str)
            refresh_daily_attendance.delay(date_str)
            
            current_date += timedelta(days=1)

        # Monthly snapshots
        current_month = start_date.replace(day=1)
        while current_month <= end_date:
            self.stdout.write(f"Processing month {current_month.year}-{current_month.month}...")
            refresh_monthly_enrollment.delay(current_month.year, current_month.month)
            
            # Move to next month
            if current_month.month == 12:
                current_month = current_month.replace(year=current_month.year + 1, month=1)
            else:
                current_month = current_month.replace(month=current_month.month + 1)

        # Coach performance (single run for the whole period)
        refresh_coach_performance.delay(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))

        self.stdout.write(self.style.SUCCESS("Successfully queued historical analytics tasks."))
