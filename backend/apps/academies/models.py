from django.db import models
from apps.common.models import UUIDModel, TimeStampedModel, SoftDeleteModel

class Academy(UUIDModel, TimeStampedModel, SoftDeleteModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    domain = models.CharField(max_length=255, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    settings = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name_plural = "Academies"

    def __str__(self):
        return self.name
