import csv
import io
import logging

from celery import shared_task
from django.core.mail import EmailMessage
from django.db.models import Sum
from django.utils import timezone

from .models import Invoice, Payment

logger = logging.getLogger(__name__)


@shared_task
def export_financial_report(academy_id, user_email):
    """
    Asynchronously generates a financial report and emails it to the user.
    """
    payments = Payment.objects.filter(academy_id=academy_id).select_related(
        "invoice__player", "recorded_by"
    )

    csv_buffer = io.StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerow(
        ["Payment ID", "Date", "Amount", "Method", "Player", "Invoice ID", "Recorded By"]
    )

    for p in payments:
        writer.writerow(
            [
                p.id,
                p.payment_date.strftime("%Y-%m-%d %H:%M:%S"),
                str(p.amount),
                p.get_method_display(),
                f"{p.invoice.player.first_name} {p.invoice.player.last_name}",
                p.invoice.id,
                p.recorded_by.username,
            ]
        )

    email = EmailMessage(
        subject="SAMS Financial Report",
        body="Please find attached the requested financial report.",
        from_email="noreply@sams.local",
        to=[user_email],
    )
    email.attach("financial_report.csv", csv_buffer.getvalue(), "text/csv")
    email.send(fail_silently=True)


@shared_task(name="apps.payments.tasks.check_overdue_invoices")
def check_overdue_invoices():
    """
    Daily task: mark unpaid invoices past their due_date as 'overdue'.
    """
    today = timezone.now().date()
    overdue_count = Invoice.objects.filter(
        status__in=["unpaid", "partially_paid"],
        due_date__lt=today,
    ).update(status="overdue")
    logger.info(f"Marked {overdue_count} invoice(s) as overdue")
    return overdue_count
