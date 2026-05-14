from apps.common.models import TimeStampedModel, UUIDModel
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser, UUIDModel, TimeStampedModel):
    id = UUIDModel.id  # Override to ensure UUID
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    preferred_language = models.CharField(max_length=5, default="en", choices=[("en", "English"), ("ar", "Arabic")])

    # A user can belong to multiple academies
    academies = models.ManyToManyField("academies.Academy", related_name="users")

    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username
