import logging
from celery import shared_task
from django.utils import timezone
from apps.reports.models import GeneratedReport, ScheduledReport
from apps.reports.generators import CSVReportGenerator, ExcelReportGenerator, PDFReportGenerator
from apps.notifications.services.notification_service import NotificationService

logger = logging.getLogger(__name__)

FORMAT_MAP = {
    "csv": CSVReportGenerator,
    "xlsx": ExcelReportGenerator,
    "pdf": PDFReportGenerator,
}

@shared_task(name="apps.reports.tasks.generate_report_task")
def generate_report_task(report_id, scheduled_report_id=None):
    try:
        report = GeneratedReport.all_objects.get(id=report_id)
    except GeneratedReport.DoesNotExist:
        logger.error(f"GeneratedReport {report_id} not found")
        return

    report.status = "processing"
    report.save()

    try:
        generator_class = FORMAT_MAP.get(report.format)
        if not generator_class:
            raise ValueError(f"Unsupported format: {report.format}")

        generator = generator_class(report)
        content_file = generator.generate()

        filename = f"{report.report_type}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.{report.format}"
        report.file.save(filename, content_file)

        report.status = "completed"
        report.save()

        # Notify user if requested
        if report.requested_by:
            NotificationService.send_notification(
                user=report.requested_by,
                template_code="GENERAL_ANNOUNCEMENT",
                context_data={
                    "title": "Report Ready",
                    "content": f"Your {report.get_report_type_display()} in {report.format} format is ready for download."
                },
                academy_id=str(report.academy_id)
            )

        # Email scheduled report recipients
        if scheduled_report_id:
            _email_report_to_recipients(report, scheduled_report_id)

    except Exception as e:
        logger.error(f"Error generating report {report_id}: {str(e)}")
        report.status = "failed"
        report.error_message = str(e)
        report.save()

def _email_report_to_recipients(report, scheduled_report_id):
    try:
        scheduled = ScheduledReport.all_objects.get(id=scheduled_report_id)
    except ScheduledReport.DoesNotExist:
        return

    recipients = scheduled.recipients
    if not recipients:
        return

    from django.core.mail import EmailMessage

    subject = f"{scheduled.name} - {report.get_report_type_display()}"
    body = f"Your scheduled report '{scheduled.name}' is ready.\n\n"
    body += f"Type: {report.get_report_type_display()}\n"
    body += f"Format: {report.format}\n"
    body += f"Generated: {timezone.now().strftime('%Y-%m-%d %H:%M')}\n"

    email = EmailMessage(
        subject=subject,
        body=body,
        to=recipients,
    )
    if report.file:
        email.attach_file(report.file.path)

    email.send(fail_silently=True)
    logger.info(f"Sent scheduled report {report.id} to {len(recipients)} recipients")


@shared_task(name="apps.reports.tasks.process_scheduled_reports")
def process_scheduled_reports():
    now = timezone.now()
    scheduled = ScheduledReport.objects.filter(is_active=True)
    
    for item in scheduled:
        # Simple check for frequency (this should be more robust with crontab or rrule)
        # For now, let's just trigger it if it hasn't been run today/this week/this month
        should_run = False
        if not item.last_run_at:
            should_run = True
        else:
            diff = now - item.last_run_at
            if item.frequency == "daily" and diff.days >= 1:
                should_run = True
            elif item.frequency == "weekly" and diff.days >= 7:
                should_run = True
            elif item.frequency == "monthly" and diff.days >= 30:
                should_run = True
                
        if should_run:
            # Create a GeneratedReport instance
            report = GeneratedReport.objects.create(
                academy=item.academy,
                report_type=item.report_type,
                format=item.format,
                parameters=item.parameters,
                status="pending"
            )
            
            item.last_run_at = now
            item.save()
            
            generate_report_task.delay(str(report.id), str(item.id))
