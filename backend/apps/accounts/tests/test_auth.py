from apps.academies.models import Academy
from apps.accounts.models import User
from apps.accounts.views.auth import ProfileView
from apps.common.thread_local import set_current_academy_id
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate


class TestProfileView(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.academy = Academy.objects.create(name="Test Academy")
        self.user = User.objects.create_user(
            username="tester", email="tester@test.com", password="testpass123"
        )
        set_current_academy_id(str(self.academy.id))

    def tearDown(self):
        set_current_academy_id(None)

    def test_profile_view_returns_user_data(self):
        req = self.factory.get("/api/v1/accounts/profile/")
        force_authenticate(req, user=self.user)
        view = ProfileView.as_view()
        response = view(req)
        assert response.status_code == 200
        assert response.data["username"] == "tester"

    def test_profile_view_requires_auth(self):
        from django.contrib.auth.models import AnonymousUser

        req = self.factory.get("/api/v1/accounts/profile/")
        req.user = AnonymousUser()
        view = ProfileView.as_view()
        response = view(req)
        assert response.status_code == 401

    def test_profile_patch_updates_user(self):
        req = self.factory.patch(
            "/api/v1/accounts/profile/",
            {"first_name": "Updated"},
            format="json",
        )
        force_authenticate(req, user=self.user)
        view = ProfileView.as_view()
        response = view(req)
        assert response.status_code == 200
        self.user.refresh_from_db()
        assert self.user.first_name == "Updated"
