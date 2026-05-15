import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.academies.models import Academy
from apps.permissions.models import Role, UserRole
from apps.players.models import Player
from apps.sessions.models import Venue, SessionSeries, SessionOccurrence, SessionCoach
from apps.attendance.models import Attendance
from apps.payments.models import Payment, Invoice
from apps.ratings.models import PlayerRating
from apps.cancellations.models import CancellationRequest

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with initial data for SAMS'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting database seeding...")

        # 1. Clear existing data (optional, be careful in prod)
        self.stdout.write("Clearing old data...")
        Payment.objects.all().delete()
        Invoice.objects.all().delete()
        Attendance.objects.all().delete()
        PlayerRating.objects.all().delete()
        CancellationRequest.objects.all().delete()
        SessionOccurrence.objects.all().delete()
        SessionSeries.objects.all().delete()
        Player.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()
        Academy.objects.all().delete()
        Role.objects.all().delete()
        Venue.objects.all().delete()

        # 2. Setup Roles
        roles = {
            "Super Admin": Role.objects.create(name=Role.SUPER_ADMIN, description="Full system access"),
            "Admin": Role.objects.create(name=Role.ADMIN, description="Academy admin"),
            "Operations": Role.objects.create(name=Role.OPERATIONS, description="Operations staff"),
            "Coach": Role.objects.create(name=Role.COACH, description="Academy coach"),
            "Customer": Role.objects.create(name=Role.CUSTOMER, description="Customer / Player parent"),
        }

        # 3. Setup Academy
        academy = Academy.objects.create(
            name="Elite Sports Academy",
            slug="elite",
            domain="elite.sams.com"
        )

        # 4. Create Users
        self.stdout.write("Creating users...")
        users = []
        # Operations
        ops_user = User.objects.create_user(username="ops", password="password123", email="ops@sams.com", first_name="Admin", last_name="User")
        UserRole.objects.create(user=ops_user, academy=academy, role=roles["Operations"])
        users.append(ops_user)

        # Coach
        coach_user = User.objects.create_user(username="coach", password="password123", email="coach@sams.com", first_name="Ahmed", last_name="Salah")
        UserRole.objects.create(user=coach_user, academy=academy, role=roles["Coach"])
        users.append(coach_user)

        # Customers (Players)
        customers = []
        for i in range(1, 11):
            cust = User.objects.create_user(
                username=f"customer{i}", password="password123", email=f"customer{i}@sams.com", 
                first_name=f"Player{i}", last_name="Smith"
            )
            UserRole.objects.create(user=cust, academy=academy, role=roles["Customer"])
            # Create player profile
            player = Player.objects.create(
                academy=academy,
                first_name=cust.first_name,
                last_name=cust.last_name,
                birth_date=timezone.now().date() - timedelta(days=365*random.randint(10, 18)),
                registration_number=f"SAMS-2026-{i:03d}"
            )
            customers.append(player)

        # 5. Create Venues and Sessions
        self.stdout.write("Creating sessions and venues...")
        venue1 = Venue.objects.create(academy=academy, name="Pitch 01", location="North Wing", capacity=30)
        venue2 = Venue.objects.create(academy=academy, name="Indoor Hall", location="Main Building", capacity=50)

        series1 = SessionSeries.objects.create(
            academy=academy, title="Football Tactical U16", start_date=timezone.now().date(), end_date=timezone.now().date() + timedelta(days=30),
            start_time="16:00:00", end_time="17:30:00", venue=venue1, max_capacity=30, recurrence_rule="FREQ=WEEKLY;BYDAY=MO,WE"
        )
        
        # Occurrences
        occurrences = []
        for i in range(5):
            occ = SessionOccurrence.objects.create(
                academy=academy,
                series=series1,
                start_datetime=timezone.now() + timedelta(days=i*2),
                end_datetime=timezone.now() + timedelta(days=i*2, hours=1, minutes=30),
                venue=venue1,
                max_capacity=30,
                status="live" if i == 0 else "scheduled"
            )
            SessionCoach.objects.create(academy=academy, session=occ, coach=coach_user, is_lead=True)
            occurrences.append(occ)

        # 6. Create Attendance, Ratings, Payments, Cancellations
        self.stdout.write("Creating operational data...")
        for player in customers:
            # Attendance for the first occurrence
            Attendance.objects.create(
                academy=academy,
                occurrence=occurrences[0], player=player,
                status=random.choice(["present", "absent", "late"]),
                marked_by=coach_user
            )

            # Rating
            PlayerRating.objects.create(
                academy=academy,
                occurrence=occurrences[0],
                player=player, coach=coach_user,
                technique=random.randint(3, 5), stamina=random.randint(3, 5), teamwork=random.randint(3, 5),
                performance_notes="Good progress overall."
            )

            # Payments & Invoices
            inv = Invoice.objects.create(
                academy=academy,
                player=player,
                description="Monthly Subscription",
                total_amount=1200.00,
                balance_due=0 if random.choice([True, False]) else 1200.00,
                due_date=timezone.now().date(),
                status=random.choice(["paid", "unpaid", "paid"])
            )
            
            if inv.status == "paid":
                Payment.objects.create(
                    academy=academy,
                    invoice=inv,
                    amount=1200.00,
                    method="cash",
                    recorded_by=ops_user,
                    is_approved=True,
                    approved_by=ops_user
                )

            # Cancellations
            if random.choice([True, False, False]):
                CancellationRequest.objects.create(
                    academy=academy,
                    occurrence=occurrences[1], player=player,
                    reason="Medical reason",
                    status="pending"
                )

        self.stdout.write(self.style.SUCCESS("Successfully seeded database!"))
        self.stdout.write("Test Users:")
        self.stdout.write("Ops: ops / password123")
        self.stdout.write("Coach: coach / password123")
        self.stdout.write("Customer: customer1 / password123")
