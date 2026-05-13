import pytest
from django.urls import reverse
from rest_framework import status
from apps.academies.models import Academy
from apps.accounts.models import User
from apps.players.models import Player
from apps.permissions.models import Role, UserRole
from apps.common.thread_local import set_current_academy_id, clear_current_academy_id

@pytest.fixture
def academy_a(db):
    return Academy.objects.create(name="Academy A", slug="academy-a")

@pytest.fixture
def academy_b(db):
    return Academy.objects.create(name="Academy B", slug="academy-b")

@pytest.fixture
def user_a(db, academy_a):
    user = User.objects.create_user(username="user_a", email="a@test.com", password="password")
    role, _ = Role.objects.get_or_create(name="Member", slug="member")
    UserRole.objects.create(user=user, academy=academy_a, role=role)
    return user

@pytest.mark.django_db
class TestMultiTenancyIsolation:
    
    def test_query_isolation(self, academy_a, academy_b):
        # Create players in both academies
        set_current_academy_id(str(academy_a.id))
        Player.objects.create(first_name="Player", last_name="A", birth_date="2010-01-01")
        
        set_current_academy_id(str(academy_b.id))
        Player.objects.create(first_name="Player", last_name="B", birth_date="2010-01-01")
        
        # Verify isolation for Academy A
        set_current_academy_id(str(academy_a.id))
        assert Player.objects.count() == 1
        assert Player.objects.first().first_name == "Player"
        assert Player.objects.first().last_name == "A"
        
        # Verify isolation for Academy B
        set_current_academy_id(str(academy_b.id))
        assert Player.objects.count() == 1
        assert Player.objects.first().last_name == "B"
        
        clear_current_academy_id()

    def test_cross_tenant_leak_prevention(self, academy_a, academy_b):
        set_current_academy_id(str(academy_a.id))
        p1 = Player.objects.create(first_name="A", last_name="A", birth_date="2010-01-01")
        
        set_current_academy_id(str(academy_b.id))
        # Attempting to fetch p1 from Academy B context should fail or return nothing
        assert Player.objects.filter(id=p1.id).exists() is False
        
        clear_current_academy_id()

    def test_automatic_tenant_injection(self, academy_a):
        set_current_academy_id(str(academy_a.id))
        player = Player.objects.create(first_name="Auto", last_name="Inject", birth_date="2010-01-01")
        assert player.academy_id == academy_a.id
        clear_current_academy_id()
