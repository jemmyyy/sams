from django.core.management.base import BaseCommand
from apps.notifications.models import NotificationTemplate

class Command(BaseCommand):
    help = "Initialize default notification templates"

    def handle(self, *args, **options):
        templates = [
            {
                "code": "PAYMENT_REMINDER",
                "name": "Payment Reminder",
                "subject_en": "Payment Reminder: {{ invoice_number }}",
                "subject_ar": "تذكير بالدفع: {{ invoice_number }}",
                "content_en": "Dear {{ name }}, this is a reminder for your invoice {{ invoice_number }} of {{ amount }} EGP.",
                "content_ar": "عزيزي {{ name }}، هذا تذكير بفاتورتك {{ invoice_number }} بمبلغ {{ amount }} جنيه.",
                "channels": ["email", "whatsapp", "in_app"]
            },
            {
                "code": "SESSION_CANCELLED",
                "name": "Session Cancelled",
                "subject_en": "Session Cancelled: {{ session_date }}",
                "subject_ar": "إلغاء الحصة: {{ session_date }}",
                "content_en": "The training session scheduled for {{ session_date }} at {{ session_time }} has been cancelled.",
                "content_ar": "تم إلغاء حصة التدريب المقررة بتاريخ {{ session_date }} في تمام الساعة {{ session_time }}.",
                "channels": ["email", "whatsapp", "push", "in_app"]
            },
            {
                "code": "PAYMENT_SUCCESS",
                "name": "Payment Success",
                "subject_en": "Payment Received: {{ invoice_number }}",
                "subject_ar": "تم استلام الدفع: {{ invoice_number }}",
                "content_en": "Thank you! We have received your payment of {{ amount }} EGP for invoice {{ invoice_number }}.",
                "content_ar": "شكراً لك! لقد استلمنا دفعتك بمبلغ {{ amount }} جنيه للفاتورة {{ invoice_number }}.",
                "channels": ["email", "in_app"]
            },
            {
                "code": "GENERAL_ANNOUNCEMENT",
                "name": "General Announcement",
                "subject_en": "New Announcement: {{ title }}",
                "subject_ar": "إعلان جديد: {{ title }}",
                "content_en": "{{ content }}",
                "content_ar": "{{ content }}",
                "channels": ["in_app"]
            }
        ]

        for t_data in templates:
            obj, created = NotificationTemplate.objects.update_or_create(
                code=t_data["code"],
                defaults=t_data
            )
            status = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"{status} template: {obj.code}"))
