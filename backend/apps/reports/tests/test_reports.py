from apps.academies.models import Academy
from apps.accounts.models import User
from apps.common.thread_local import set_current_academy_id
from apps.reports.generators import CSVReportGenerator
from apps.reports.models import GeneratedReport
from apps.reports.tasks import generate_report_task
from django.test import TestCase


class TestReportGenerators(TestCase):
    def setUp(self):
        self.academy = Academy.objects.create(name="Test Academy")
        set_current_academy_id(str(self.academy.id))
        self.user = User.objects.create_user(
            username="reporter", email="reporter@test.com", password="testpass123"
        )

    def tearDown(self):
        set_current_academy_id(None)

    def _make_report(self, report_type="financial", format="csv", parameters=None):
        return GeneratedReport.objects.create(
            academy=self.academy,
            report_type=report_type,
            format=format,
            parameters=parameters or {},
            requested_by=self.user,
        )

    def test_get_data_financial(self):
        report = self._make_report("financial", "csv")
        gen = CSVReportGenerator(report)
        data = gen.get_data()
        assert isinstance(data, list)

    def test_get_data_attendance(self):
        report = self._make_report("attendance", "csv")
        gen = CSVReportGenerator(report)
        data = gen.get_data()
        assert isinstance(data, list)

    def test_get_data_utilization(self):
        report = self._make_report("utilization", "csv")
        gen = CSVReportGenerator(report)
        data = gen.get_data()
        assert isinstance(data, list)

    def test_get_data_performance(self):
        report = self._make_report("performance", "csv")
        gen = CSVReportGenerator(report)
        data = gen.get_data()
        assert isinstance(data, list)

    def test_get_data_unknown_type(self):
        report = self._make_report("unknown_type", "csv")
        gen = CSVReportGenerator(report)
        data = gen.get_data()
        assert data == []

    def test_csv_generator_creates_content_file(self):
        report = self._make_report("financial", "csv")
        gen = CSVReportGenerator(report)
        result = gen.generate()
        assert result is not None

    def test_generate_report_task_updates_status(self):
        report = self._make_report("financial", "csv")
        generate_report_task(str(report.id))
        report.refresh_from_db()
        assert report.status in ("completed", "failed")

    def test_generate_report_task_unknown_format_fails(self):
        report = self._make_report("financial", "xyz")
        generate_report_task(str(report.id))
        report.refresh_from_db()
        assert report.status == "failed"
