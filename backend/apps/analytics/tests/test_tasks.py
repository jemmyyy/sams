import pytest
from datetime import date, timedelta
from django.utils import timezone
from apps.academies.models import Academy
from apps.payments.models import Invoice, Payment
from apps.players.models import Player
from apps.analytics.models import DailyRevenueSnapshot
from apps.analytics.tasks import refresh_daily_revenue
from decimal import Decimal

@pytest.fixture
def academy(db):
    return Academy.objects.create(name="Analytics Academy", slug="analytics-academy")

@pytest.fixture
def player(academy):
    return Player.objects.create(
        academy=academy,
        first_name="John",
        last_name="Doe",
        birth_date="2000-01-01",
        registration_number="REG001"
    )

@pytest.fixture
def user(db):
    from apps.accounts.models import User
    return User.objects.create_user(username="admin_user", email="admin@test.com", password="password")

@pytest.mark.django_db
def test_refresh_daily_revenue_task(academy, player, user):
    # Create a payment for yesterday
    yesterday = timezone.now().date() - timedelta(days=1)
    
    invoice = Invoice.objects.create(
        academy=academy,
        player=player,
        description="Test Invoice",
        total_amount=Decimal("100.00"),
        balance_due=Decimal("0.00"),
        due_date=yesterday
    )
    
    # We need to manually set payment_date because of auto_now_add
    # But wait, refresh_daily_revenue uses payment_date__date
    # Let's mock the auto_now_add or just use update after create
    payment = Payment.objects.create(
        academy=academy,
        invoice=invoice,
        amount=Decimal("100.00"),
        method="cash",
        recorded_by=user,
        is_approved=True
    )
    Payment.objects.filter(id=payment.id).update(payment_date=timezone.make_aware(timezone.datetime.combine(yesterday, timezone.datetime.min.time())))
    
    # Run task
    refresh_daily_revenue()
    
    # Verify snapshot
    snapshot = DailyRevenueSnapshot.objects.get(academy=academy, date=yesterday)
    assert snapshot.total_income == Decimal("100.00")
    assert snapshot.payment_count == 1
    assert snapshot.net_revenue == Decimal("100.00")
