from apps.common.models import SoftDeleteModel, TimeStampedModel, UUIDModel
from django.db import models


class Academy(UUIDModel, TimeStampedModel, SoftDeleteModel):
    SUBSCRIPTION_CHOICES = [
        ("free", "Free"),
        ("basic", "Basic"),
        ("premium", "Premium"),
        ("enterprise", "Enterprise"),
    ]
    STATUS_CHOICES = [
        ("active", "Active"),
        ("suspended", "Suspended"),
        ("trialing", "Trialing"),
        ("cancelled", "Cancelled"),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    domain = models.CharField(max_length=255, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    subscription_plan = models.CharField(max_length=20, choices=SUBSCRIPTION_CHOICES, default="free")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    branding_settings = models.JSONField(default=dict, blank=True)
    timezone = models.CharField(max_length=50, default="Africa/Cairo")
    language = models.CharField(max_length=5, default="ar", choices=[("ar", "Arabic"), ("en", "English")])
    currency = models.CharField(max_length=3, default="EGP")
    settings = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name_plural = "Academies"

    def __str__(self):
        return self.name
