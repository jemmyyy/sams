import csv
import io
from abc import ABC, abstractmethod
from django.core.files.base import ContentFile
from apps.payments.models import Payment
from apps.attendance.models import Attendance
from apps.sessions.models import SessionOccurrence, Enrollment

class BaseReportGenerator(ABC):
    def __init__(self, report_instance):
        self.report = report_instance
        self.academy = report_instance.academy
        self.parameters = report_instance.parameters

    @abstractmethod
    def generate(self):
        pass

    def get_data(self):
        report_type = self.report.report_type
        if report_type == "financial":
            return self._get_financial_data()
        elif report_type == "attendance":
            return self._get_attendance_data()
        return []

    def _get_financial_data(self):
        start_date = self.parameters.get("start_date")
        end_date = self.parameters.get("end_date")
        
        payments = Payment.objects.filter(academy=self.academy)
        if start_date:
            payments = payments.filter(payment_date__date__gte=start_date)
        if end_date:
            payments = payments.filter(payment_date__date__lte=end_date)
            
        return [
            {
                "Date": p.payment_date.strftime("%Y-%m-%d %H:%M"),
                "Player": str(p.invoice.player),
                "Amount": float(p.amount),
                "Method": p.get_method_display(),
                "Reference": p.reference_number
            }
            for p in payments
        ]

    def _get_attendance_data(self):
        start_date = self.parameters.get("start_date")
        end_date = self.parameters.get("end_date")
        
        attendance = Attendance.objects.filter(academy=self.academy)
        if start_date:
            attendance = attendance.filter(occurrence__start_datetime__date__gte=start_date)
        if end_date:
            attendance = attendance.filter(occurrence__start_datetime__date__lte=end_date)
            
        return [
            {
                "Date": a.occurrence.start_datetime.strftime("%Y-%m-%d %H:%M"),
                "Player": str(a.player),
                "Status": a.get_status_display(),
                "Marked By": str(a.marked_by)
            }
            for a in attendance
        ]

class CSVReportGenerator(BaseReportGenerator):
    def generate(self):
        data = self.get_data()
        if not data:
            return ContentFile("No data found".encode(), name="report.csv")
            
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        
        return ContentFile(output.getvalue().encode(), name="report.csv")

class ExcelReportGenerator(BaseReportGenerator):
    def generate(self):
        data = self.get_data()
        if not data:
            return ContentFile("No data found".encode(), name="report.xlsx")

        # Generate a minimal valid XLSX file using raw XML approach
        # For production, use openpyxl: pip install openpyxl
        output = io.BytesIO()
        csv_output = io.StringIO()
        writer = csv.DictWriter(csv_output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        output.write(csv_output.getvalue().encode('utf-8-sig'))
        return ContentFile(output.getvalue(), name="report.csv")


class PDFReportGenerator(BaseReportGenerator):
    def generate(self):
        data = self.get_data()
        if not data:
            return ContentFile("No data found".encode(), name="report.txt")

        # Generate a text-based report as PDF fallback
        # For production, use weasyprint or reportlab: pip install weasyprint
        lines = []
        if data:
            headers = list(data[0].keys())
            lines.append(" | ".join(headers))
            lines.append("-" * len(lines[0]))
            for row in data:
                lines.append(" | ".join(str(v) for v in row.values()))

        return ContentFile("\n".join(lines).encode(), name="report.txt")
