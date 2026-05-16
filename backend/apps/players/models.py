from apps.common.models import TenantAwareModel
from django.db import models


class Player(TenantAwareModel):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
        OTHER = "other", "Other"

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    registration_number = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    photo = models.ImageField(upload_to="players/photos/", blank=True)
    gender = models.CharField(max_length=10, choices=Gender.choices, blank=True)
    medical_notes = models.TextField(blank=True)
    emergency_contact = models.JSONField(default=dict, blank=True)
    parent = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )

    class Meta:
        unique_together = ("academy", "registration_number")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
