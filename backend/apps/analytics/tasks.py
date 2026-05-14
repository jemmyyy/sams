import logging
from celery import shared_task
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from apps.academies.models import Academy
from apps.payments.models import Payment, Refund
from apps.attendance.models import Attendance
from apps.sessions.models import SessionOccurrence, SessionCoach, Enrollment
from apps.reports.models import SessionReport
from .models import (
    DailyRevenueSnapshot, 
    DailyAttendanceSnapshot, 
    CoachPerformanceSnapshot,
    MonthlyEnrollmentSnapshot
)

logger = logging.getLogger(__name__)

@shared_task(name="apps.analytics.tasks.refresh_monthly_enrollment")
def refresh_monthly_enrollment(year=None, month=None):
    if year is None or month is None:
        now = timezone.now()
        year = now.year
        month = now.month

    for academy in Academy.objects.filter(is_active=True):
        # Active players (simplified: anyone with an active enrollment this month)
        total_active = Enrollment.objects.filter(
            academy=academy,
            status='active',
            session__start_datetime__year=year,
            session__start_datetime__month=month
        ).values('player').distinct().count()
        
        # New enrollments this month
        new_enrolls = Enrollment.objects.filter(
            academy=academy,
            enrolled_at__year=year,
            enrolled_at__month=month
        ).values('player').distinct().count()
        
        # Churned (simplified: players who were active last month but not this month)
        # This is more complex in a real SaaS, but for now:
        last_month = month - 1 if month > 1 else 12
        last_year = year if month > 1 else year - 1
        
        active_last_month = set(Enrollment.objects.filter(
            academy=academy,
            session__start_datetime__year=last_year,
            session__start_datetime__month=last_month
        ).values_list('player_id', flat=True))
        
        active_this_month = set(Enrollment.objects.filter(
            academy=academy,
            session__start_datetime__year=year,
            session__start_datetime__month=month
        ).values_list('player_id', flat=True))
        
        churned = len(active_last_month - active_this_month)
        
        MonthlyEnrollmentSnapshot.objects.update_or_create(
            academy=academy,
            year=year,
            month=month,
            defaults={
                'total_active_players': total_active,
                'new_enrollments': new_enrolls,
                'churned_players': churned
            }
        )

@shared_task(name="apps.analytics.tasks.refresh_daily_revenue")
def refresh_daily_revenue(date_str=None):
    if date_str:
        date = timezone.datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        date = timezone.now().date() - timedelta(days=1)

    for academy in Academy.objects.filter(is_active=True):
        payments = Payment.objects.filter(
            academy=academy,
            payment_date__date=date,
            is_approved=True
        ).aggregate(
            total=Sum('amount'),
            count=Count('id')
        )
        
        refunds = Refund.objects.filter(
            academy=academy,
            status='approved',
            updated_at__date=date # Assuming approval date is what matters
        ).aggregate(total=Sum('amount'))

        total_income = payments['total'] or 0
        total_refunds = refunds['total'] or 0
        
        DailyRevenueSnapshot.objects.update_or_create(
            academy=academy,
            date=date,
            defaults={
                'total_income': total_income,
                'total_refunds': total_refunds,
                'net_revenue': total_income - total_refunds,
                'payment_count': payments['count'] or 0
            }
        )

@shared_task(name="apps.analytics.tasks.refresh_daily_attendance")
def refresh_daily_attendance(date_str=None):
    if date_str:
        date = timezone.datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        date = timezone.now().date() - timedelta(days=1)

    for academy in Academy.objects.filter(is_active=True):
        occurrences = SessionOccurrence.objects.filter(
            academy=academy,
            start_datetime__date=date,
            status='completed'
        )
        
        total_expected = 0
        total_present = 0
        
        for occ in occurrences:
            expected = occ.enrollments.count()
            present = occ.attendance_records.filter(status='present').count()
            total_expected += expected
            total_present += present
            
        total_absent = total_expected - total_present
        rate = (total_present / total_expected * 100) if total_expected > 0 else 0
        
        DailyAttendanceSnapshot.objects.update_or_create(
            academy=academy,
            date=date,
            defaults={
                'total_expected': total_expected,
                'total_present': total_present,
                'total_absent': total_absent,
                'attendance_rate': rate
            }
        )

@shared_task(name="apps.analytics.tasks.refresh_coach_performance")
def refresh_coach_performance(period_start_str=None, period_end_str=None):
    # Default to last 30 days
    if period_start_str and period_end_str:
        start_date = timezone.datetime.strptime(period_start_str, "%Y-%m-%d").date()
        end_date = timezone.datetime.strptime(period_end_str, "%Y-%m-%d").date()
    else:
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)

    for academy in Academy.objects.filter(is_active=True):
        coaches = academy.users.filter(user_roles__role__name='coach').distinct()
        
        for coach in coaches:
            # Sessions conducted
            session_ids = SessionCoach.objects.filter(
                coach=coach,
                session__start_datetime__date__range=(start_date, end_date),
                session__status='completed'
            ).values_list('session_id', flat=True)
            
            sessions_count = len(session_ids)
            
            # Attendance rate for those sessions
            attendance_stats = Attendance.objects.filter(
                occurrence_id__in=session_ids
            ).aggregate(
                total=Count('id'),
                present=Count('id', filter=Q(status='present'))
            )
            
            total_att = attendance_stats['total']
            present_att = attendance_stats['present']
            avg_rate = (present_att / total_att * 100) if total_att > 0 else 0
            
            # Reports submitted
            reports_count = SessionReport.objects.filter(
                coach=coach,
                occurrence_id__in=session_ids
            ).count()
            
            CoachPerformanceSnapshot.objects.update_or_create(
                academy=academy,
                coach=coach,
                period_start=start_date,
                period_end=end_date,
                defaults={
                    'sessions_conducted': sessions_count,
                    'average_attendance_rate': avg_rate,
                    'reports_submitted': reports_count
                }
            )
