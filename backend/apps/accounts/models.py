from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.common.models import UUIDModel, TimeStampedModel

class User(AbstractUser, UUIDModel, TimeStampedModel):
    id = UUIDModel.id # Override to ensure UUID
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    
    # A user can belong to multiple academies with different roles
    academies = models.ManyToManyField(
        'academies.Academy',
        through='permissions.UserRole',
        related_name='users'
    )

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
