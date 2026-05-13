from apps.common.models import TimeStampedModel, UUIDModel
from django.db import models


class Role(UUIDModel, TimeStampedModel):
    # Standard roles: CUSTOMER, COACH, OPERATIONS, ADMIN, SUPER_ADMIN
    CUSTOMER = "customer"
    COACH = "coach"
    OPERATIONS = "operations"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

    ROLE_CHOICES = [
        (CUSTOMER, "Customer"),
        (COACH, "Coach"),
        (OPERATIONS, "Operations"),
        (ADMIN, "Admin"),
        (SUPER_ADMIN, "Super Admin"),
    ]

    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True)
    permissions = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.get_name_display()


class UserRole(UUIDModel, TimeStampedModel):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="user_roles")
    academy = models.ForeignKey(
        "academies.Academy", on_delete=models.CASCADE, related_name="user_roles"
    )
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "academy", "role")

    def __str__(self):
        return f"{self.user.username} - {self.role.name} @ {self.academy.name}"
