from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.academies.models import Academy
from apps.permissions.models import Role, UserRole

User = get_user_model()

class Command(BaseCommand):
    help = "Create test accounts for Coach and Operations"

    def handle(self, *args, **options):
        # 1. Ensure Academy exists
        academy, _ = Academy.objects.get_or_create(
            slug="test-academy",
            defaults={"name": "Test Academy"}
        )
        self.stdout.write(f"Using Academy: {academy.name}")

        # 2. Ensure Roles exist
        roles = {}
        for role_name, role_display in Role.ROLE_CHOICES:
            role, _ = Role.objects.get_or_create(name=role_name)
            roles[role_name] = role

        # 3. Create Coach Account
        coach_user, created = User.objects.get_or_create(
            username="coach_test",
            defaults={
                "email": "coach@test.com",
                "first_name": "Test",
                "last_name": "Coach",
                "is_staff": True
            }
        )
        if created:
            coach_user.set_password("sams_coach_123")
            coach_user.save()
            self.stdout.write(self.style.SUCCESS("Created Coach user: coach_test"))
        
        coach_user.academies.add(academy)
        UserRole.objects.get_or_create(user=coach_user, academy=academy, role=roles[Role.COACH])

        # 4. Create Operations Account
        ops_user, created = User.objects.get_or_create(
            username="ops_test",
            defaults={
                "email": "ops@test.com",
                "first_name": "Test",
                "last_name": "Ops",
                "is_staff": True
            }
        )
        if created:
            ops_user.set_password("sams_ops_123")
            ops_user.save()
            self.stdout.write(self.style.SUCCESS("Created Operations user: ops_test"))
        
        ops_user.academies.add(academy)
        UserRole.objects.get_or_create(user=ops_user, academy=academy, role=roles[Role.OPERATIONS])

        self.stdout.write(self.style.SUCCESS("Successfully set up test accounts."))
