from decimal import Decimal

from apps.academies.models import Academy
from apps.accounts.models import User
from apps.payments.models import Invoice, Payment, Refund
from apps.players.models import Player
from django.test import TestCase
from django.utils import timezone


class TestPaymentApproval(TestCase):
    def setUp(self):
        self.academy = Academy.objects.create(name="Test Academy")
        self.staff = User.objects.create_user(
            username="staff", email="staff@test.com", password="testpass123"
        )
        self.player = Player.objects.create(
            academy=self.academy,
            first_name="Test",
            last_name="Player",
            birth_date="2010-01-01",
            registration_number="REG001",
        )
        self.invoice = Invoice.objects.create(
            academy=self.academy,
            player=self.player,
            description="Test invoice",
            total_amount=Decimal("500.00"),
            balance_due=Decimal("500.00"),
            due_date=timezone.now().date() + timezone.timedelta(days=30),
        )

    def test_cash_payment_is_auto_approved(self):
        payment = Payment.objects.create(
            academy=self.academy,
            invoice=self.invoice,
            amount=Decimal("500.00"),
            method="cash",
            recorded_by=self.staff,
        )
        assert payment.is_approved is True

    def test_bank_transfer_payment_is_pending_approval(self):
        payment = Payment.objects.create(
            academy=self.academy,
            invoice=self.invoice,
            amount=Decimal("500.00"),
            method="bank_transfer",
            recorded_by=self.staff,
        )
        assert payment.is_approved is False

    def test_approve_bank_transfer_payment(self):
        payment = Payment.objects.create(
            academy=self.academy,
            invoice=self.invoice,
            amount=Decimal("500.00"),
            method="bank_transfer",
            recorded_by=self.staff,
        )
        approver = User.objects.create_user(
            username="admin", email="admin@test.com", password="testpass123"
        )
        payment.approve(approved_by=approver)
        payment.refresh_from_db()
        assert payment.is_approved is True
        assert payment.approved_by == approver

    def test_reject_payment(self):
        payment = Payment.objects.create(
            academy=self.academy,
            invoice=self.invoice,
            amount=Decimal("500.00"),
            method="bank_transfer",
            recorded_by=self.staff,
        )
        payment.reject(reason="Invalid reference", rejected_by=self.staff)
        payment.refresh_from_db()
        assert payment.is_approved is False
        assert "Invalid reference" in payment.notes


class TestRefundApproval(TestCase):
    def setUp(self):
        self.academy = Academy.objects.create(name="Test Academy")
        self.staff = User.objects.create_user(
            username="staff", email="staff@test.com", password="testpass123"
        )
        self.admin = User.objects.create_user(
            username="admin", email="admin@test.com", password="testpass123"
        )
        self.player = Player.objects.create(
            academy=self.academy,
            first_name="Test",
            last_name="Player",
            birth_date="2010-01-01",
            registration_number="REG001",
        )
        self.invoice = Invoice.objects.create(
            academy=self.academy,
            player=self.player,
            description="Test invoice",
            total_amount=Decimal("500.00"),
            balance_due=Decimal("0.00"),
            due_date=timezone.now().date() + timezone.timedelta(days=30),
        )
        self.payment = Payment.objects.create(
            academy=self.academy,
            invoice=self.invoice,
            amount=Decimal("500.00"),
            method="cash",
            recorded_by=self.staff,
        )

    def test_refund_approve(self):
        refund = Refund.objects.create(
            academy=self.academy,
            payment=self.payment,
            amount=Decimal("200.00"),
            reason="Duplicate payment",
            requested_by=self.staff,
        )
        assert refund.status == "pending"
        refund.approve(approved_by=self.admin)
        refund.refresh_from_db()
        assert refund.status == "approved"
        assert refund.approved_by == self.admin

    def test_refund_reject(self):
        refund = Refund.objects.create(
            academy=self.academy,
            payment=self.payment,
            amount=Decimal("500.00"),
            reason="Changed mind",
            requested_by=self.staff,
        )
        refund.reject(rejected_by=self.admin)
        refund.refresh_from_db()
        assert refund.status == "rejected"
