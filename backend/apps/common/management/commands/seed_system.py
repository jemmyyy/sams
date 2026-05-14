import random
from decimal import Decimal
from datetime import timedelta, date, time
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from apps.academies.models import Academy
from apps.permissions.models import Role, UserRole
from apps.players.models import Player
from apps.groups.models import Group, GroupCoach
from apps.sessions.models import Venue, SessionSeries, SessionOccurrence, SessionCoach, Enrollment
from apps.payments.models import Invoice, Payment, Refund
from apps.attendance.models import Attendance
from apps.notifications.models import NotificationTemplate, NotificationLog
from apps.analytics.tasks import refresh_daily_revenue, refresh_daily_attendance, refresh_monthly_enrollment, refresh_coach_performance

User = get_user_model()

class Command(BaseCommand):
    help = "Seed the entire system with realistic data for testing"

    def handle(self, *args, **options):
        self.stdout.write("Starting system seed...")

        # 1. Academies
        academies_data = [
            {"name": "Elite Sports Academy", "slug": "elite-academy", "domain": "elite.sams.com"},
            {"name": "Cairo Stars Academy", "slug": "cairo-stars", "domain": "stars.sams.com"},
        ]
        academies = []
        for a_data in academies_data:
            academy, _ = Academy.objects.get_or_create(slug=a_data["slug"], defaults=a_data)
            academies.append(academy)
            self.stdout.write(f"Academy: {academy.name}")

        # 2. Roles
        for role_name, role_display in Role.ROLE_CHOICES:
            Role.objects.get_or_create(name=role_name)

        # 3. Notification Templates
        from apps.notifications.management.commands.init_notifications import Command as InitNotify
        InitNotify().handle()

        # Seed each academy
        for academy in academies:
            self.stdout.write(f"\nSeeding data for {academy.name}...")
            
            # 4. Users & Roles
            # Admin
            admin_user, _ = User.objects.get_or_create(
                username=f"admin_{academy.slug}",
                defaults={"email": f"admin@{academy.slug}.com", "is_staff": True}
            )
            admin_user.set_password("sams123")
            admin_user.save()
            admin_user.academies.add(academy)
            UserRole.objects.get_or_create(user=admin_user, academy=academy, role=Role.objects.get(name=Role.ADMIN))

            # Operations
            ops_users = []
            for i in range(2):
                u, _ = User.objects.get_or_create(
                    username=f"ops_{i}_{academy.slug}",
                    defaults={"email": f"ops{i}@{academy.slug}.com", "is_staff": True}
                )
                u.set_password("sams123")
                u.save()
                u.academies.add(academy)
                UserRole.objects.get_or_create(user=u, academy=academy, role=Role.objects.get(name=Role.OPERATIONS))
                ops_users.append(u)

            # Coaches
            coaches = []
            coach_names = ["Ahmed", "Mohamed", "Hassan", "Youssef", "Omar"]
            for i, name in enumerate(coach_names):
                u, _ = User.objects.get_or_create(
                    username=f"coach_{i}_{academy.slug}",
                    defaults={"email": f"coach_{i}@{academy.slug}.com", "first_name": name, "last_name": "Coach", "is_staff": True}
                )
                u.set_password("sams123")
                u.save()
                u.academies.add(academy)
                UserRole.objects.get_or_create(user=u, academy=academy, role=Role.objects.get(name=Role.COACH))
                coaches.append(u)

            # Customers (Parents)
            customers = []
            for i in range(20):
                u, _ = User.objects.get_or_create(
                    username=f"parent_{i}_{academy.slug}",
                    defaults={"email": f"parent_{i}@{academy.slug}.com", "first_name": f"Parent_{i}", "last_name": academy.slug}
                )
                u.set_password("sams123")
                u.save()
                u.academies.add(academy)
                UserRole.objects.get_or_create(user=u, academy=academy, role=Role.objects.get(name=Role.CUSTOMER))
                customers.append(u)

            # 5. Players
            players = []
            for i in range(40):
                p = Player.objects.create(
                    academy=academy,
                    first_name=f"Player_{i}",
                    last_name=academy.slug,
                    birth_date=date(2010 + random.randint(0, 10), 1, 1),
                    registration_number=f"REG-{academy.slug}-{i:04d}"
                )
                players.append(p)

            # 6. Venues
            venues = [
                Venue.objects.create(academy=academy, name="Main Football Pitch", capacity=50),
                Venue.objects.create(academy=academy, name="Indoor Hall", capacity=20),
            ]

            # 7. Groups
            groups = []
            for level in ["Beginner", "Intermediate", "Advanced"]:
                g = Group.objects.create(academy=academy, name=f"Football {level}", level=level)
                # Assign some players to groups
                g.players.add(*random.sample(players, 10))
                # Assign lead coach
                GroupCoach.objects.create(academy=academy, group=g, coach=random.choice(coaches), is_lead=True)
                groups.append(g)

            # 8. Sessions (Series & Occurrences)
            series = SessionSeries.objects.create(
                academy=academy,
                title="Weekly Football Training",
                start_date=timezone.now().date() - timedelta(days=60),
                start_time=time(16, 0),
                end_time=time(18, 0),
                recurrence_rule="FREQ=WEEKLY;BYDAY=MO,WE",
                venue=venues[0],
                max_capacity=30
            )
            series.groups.add(*groups)

            # Generate occurrences for last 30 days and next 30 days
            start_point = timezone.now() - timedelta(days=30)
            for d in range(60):
                current_date = (start_point + timedelta(days=d)).date()
                if current_date.weekday() in [0, 2]: # Monday, Wednesday
                    occ = SessionOccurrence.objects.create(
                        academy=academy,
                        series=series,
                        start_datetime=timezone.make_aware(timezone.datetime.combine(current_date, time(16, 0))),
                        end_datetime=timezone.make_aware(timezone.datetime.combine(current_date, time(18, 0))),
                        venue=venues[0],
                        max_capacity=30,
                        status="completed" if current_date < timezone.now().date() else "scheduled"
                    )
                    # Assign coach
                    SessionCoach.objects.create(academy=academy, session=occ, coach=random.choice(coaches), is_lead=True)
                    
                    # Enroll players from the group
                    target_players = players[:20]
                    for p in target_players:
                        Enrollment.objects.create(academy=academy, session=occ, player=p)
                        
                        # 9. Attendance (Historical)
                        if occ.status == "completed":
                            Attendance.objects.create(
                                academy=academy,
                                occurrence=occ,
                                player=p,
                                status=random.choice(["present", "present", "present", "absent"]),
                                marked_by=random.choice(coaches)
                            )

            # 10. Financials
            for p in players:
                # One paid invoice
                inv_paid = Invoice.objects.create(
                    academy=academy,
                    player=p,
                    description="Registration Fees",
                    total_amount=Decimal("1000.00"),
                    balance_due=Decimal("0.00"),
                    due_date=timezone.now().date() - timedelta(days=45),
                    status="paid"
                )
                Payment.objects.create(
                    academy=academy,
                    invoice=inv_paid,
                    amount=Decimal("1000.00"),
                    method="cash",
                    recorded_by=random.choice(ops_users),
                    payment_date=timezone.now() - timedelta(days=44)
                )

                # One unpaid/partially paid invoice
                status = random.choice(["unpaid", "partially_paid", "overdue"])
                total = Decimal("500.00")
                balance = total if status != "partially_paid" else Decimal("200.00")
                Invoice.objects.create(
                    academy=academy,
                    player=p,
                    description="Monthly Subscription - May",
                    total_amount=total,
                    balance_due=balance,
                    due_date=timezone.now().date() - timedelta(days=5),
                    status=status
                )

        # 11. Notifications (Logs)
        for academy in academies:
            admin = User.objects.get(username=f"admin_{academy.slug}")
            NotificationLog.objects.create(
                academy=academy,
                user=admin,
                channel="in_app",
                subject="System Seed Completed",
                content=f"The system has been seeded with test data for {academy.name}.",
                status="sent"
            )

        # 12. Refresh Analytics
        self.stdout.write("\nRefreshing analytics snapshots...")
        refresh_daily_revenue.delay()
        refresh_daily_attendance.delay()
        refresh_monthly_enrollment.delay()
        refresh_coach_performance.delay()

        self.stdout.write(self.style.SUCCESS("\nSystem seeding completed successfully!"))
        self.stdout.write("Credentials for all accounts is 'sams123'")
        self.stdout.write("Example usernames: admin_elite-academy, coach_0_elite-academy, ops_0_elite-academy")
