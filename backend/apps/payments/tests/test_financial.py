import pytest
from decimal import Decimal
from django.utils import timezone
from apps.academies.models import Academy
from apps.players.models import Player
from apps.payments.models import Invoice, Payment
from apps.payments.services.financial import FinancialService
from apps.accounts.models import User

@pytest.fixture
def academy(db):
    return Academy.objects.create(name="Finance Academy", slug="finance-academy")

@pytest.fixture
def player(academy):
    return Player.objects.create(
        academy=academy,
        first_name="Rich",
        last_name="Student",
        birth_date="2010-01-01",
        registration_number="PAY-001"
    )

@pytest.fixture
def user(db):
    return User.objects.create_user(username="cashier", email="cashier@test.com", password="password")

@pytest.mark.django_db
class TestFinancialSystem:
    def test_record_payment_updates_invoice(self, academy, player, user):
        invoice = Invoice.objects.create(
            academy=academy,
            player=player,
            description="Monthly Fees",
            total_amount=Decimal('1000.00'),
            balance_due=Decimal('1000.00'),
            due_date=timezone.now().date()
        )
        
        FinancialService.record_payment(
            invoice=invoice,
            amount=Decimal('400.00'),
            method='cash',
            recorded_by=user
        )
        
        invoice.refresh_from_db()
        assert invoice.balance_due == Decimal('600.00')
        assert invoice.status == 'partially_paid'
        assert Payment.objects.filter(invoice=invoice).count() == 1

    def test_full_payment_marks_as_paid(self, academy, player, user):
        invoice = Invoice.objects.create(
            academy=academy,
            player=player,
            description="Monthly Fees",
            total_amount=Decimal('500.00'),
            balance_due=Decimal('500.00'),
            due_date=timezone.now().date()
        )
        
        FinancialService.record_payment(
            invoice=invoice,
            amount=Decimal('500.00'),
            method='cash',
            recorded_by=user
        )
        
        invoice.refresh_from_db()
        assert invoice.balance_due == Decimal('0.00')
        assert invoice.status == 'paid'

    def test_credit_adjustment(self, academy, player, user):
        invoice = Invoice.objects.create(
            academy=academy,
            player=player,
            description="Monthly Fees",
            total_amount=Decimal('1000.00'),
            balance_due=Decimal('1000.00'),
            due_date=timezone.now().date()
        )
        
        FinancialService.apply_adjustment(
            invoice=invoice,
            amount=Decimal('100.00'),
            adjustment_type='credit',
            reason="Scholarship",
            approved_by=user
        )
        
        invoice.refresh_from_db()
        assert invoice.balance_due == Decimal('900.00')
