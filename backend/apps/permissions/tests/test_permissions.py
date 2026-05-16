from apps.academies.models import Academy
from apps.accounts.models import User
from apps.permissions.models import Role, UserRole
from apps.permissions.permissions import IsAdmin, IsCoach, IsCustomer, IsOperations, IsSuperAdmin
from apps.common.thread_local import set_current_academy_id
from django.test import TestCase, RequestFactory


class TestPermissionClasses(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.academy = Academy.objects.create(name="Test Academy")
        self.superadmin = User.objects.create_user(username="sa", email="sa@test.com", password="p")
        self.superadmin.is_superuser = True
        self.superadmin.save()
        self.admin = User.objects.create_user(username="admin", email="admin@test.com", password="p")
        self.ops = User.objects.create_user(username="ops", email="ops@test.com", password="p")
        self.coach = User.objects.create_user(username="coach", email="coach@test.com", password="p")
        self.customer = User.objects.create_user(username="cust", email="cust@test.com", password="p")

        # Create roles
        Role.objects.get_or_create(name=Role.ADMIN, defaults={"description": "Admin"})
        Role.objects.get_or_create(name=Role.OPERATIONS, defaults={"description": "Ops"})
        Role.objects.get_or_create(name=Role.COACH, defaults={"description": "Coach"})
        Role.objects.get_or_create(name=Role.CUSTOMER, defaults={"description": "Customer"})

        # Assign roles
        self._assign_role(self.admin, Role.ADMIN)
        self._assign_role(self.ops, Role.OPERATIONS)
        self._assign_role(self.coach, Role.COACH)
        self._assign_role(self.customer, Role.CUSTOMER)

        set_current_academy_id(str(self.academy.id))

    def tearDown(self):
        set_current_academy_id(None)

    def _assign_role(self, user, role_name):
        role = Role.objects.get(name=role_name)
        UserRole.objects.get_or_create(user=user, academy=self.academy, role=role)

    def _make_request(self, user):
        req = self.factory.get("/")
        req.user = user
        return req

    def test_superuser_has_all_permissions(self):
        req = self._make_request(self.superadmin)
        assert IsSuperAdmin().has_permission(req, None)
        assert IsAdmin().has_permission(req, None)
        assert IsOperations().has_permission(req, None)
        assert IsCoach().has_permission(req, None)
        assert IsCustomer().has_permission(req, None)

    def test_admin_hierarchy(self):
        req = self._make_request(self.admin)
        assert not IsSuperAdmin().has_permission(req, None)
        assert IsAdmin().has_permission(req, None)
        assert IsOperations().has_permission(req, None)
        assert IsCoach().has_permission(req, None)
        assert IsCustomer().has_permission(req, None)

    def test_operations_hierarchy(self):
        req = self._make_request(self.ops)
        assert not IsSuperAdmin().has_permission(req, None)
        assert not IsAdmin().has_permission(req, None)
        assert IsOperations().has_permission(req, None)
        assert IsCoach().has_permission(req, None)
        assert IsCustomer().has_permission(req, None)

    def test_coach_hierarchy(self):
        req = self._make_request(self.coach)
        assert not IsOperations().has_permission(req, None)
        assert IsCoach().has_permission(req, None)
        assert IsCustomer().has_permission(req, None)

    def test_customer_hierarchy(self):
        req = self._make_request(self.customer)
        assert not IsCoach().has_permission(req, None)
        assert IsCustomer().has_permission(req, None)

    def test_unauthenticated_denied(self):
        from django.contrib.auth.models import AnonymousUser
        req = self.factory.get("/")
        req.user = AnonymousUser()
        assert not IsCustomer().has_permission(req, None)
