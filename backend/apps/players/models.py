from django.db import models
from apps.common.models import TenantAwareModel

class Player(TenantAwareModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    registration_number = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
