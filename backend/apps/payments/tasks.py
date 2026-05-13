import csv
import io

from celery import shared_task
from django.core.mail import EmailMessage

from .models import Payment


@shared_task
def export_financial_report(academy_id, user_email):
    """
    Asynchronously generates a financial report and emails it to the user.
    """
    # Simple CSV export of payments for the given academy
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
