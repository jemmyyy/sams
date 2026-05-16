import uuid

from django.db import models
from django.utils import timezone

from .thread_local import get_current_academy_id


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super().delete()

    class Meta:
        abstract = True


class TenantManager(SoftDeleteManager):
    def get_queryset(self):
        qs = super().get_queryset()
        academy_id = get_current_academy_id()
        if academy_id:
            return qs.filter(academy_id=academy_id)
        return qs.none()


class TenantAwareModel(UUIDModel, TimeStampedModel, SoftDeleteModel):
    academy = models.ForeignKey(
        "academies.Academy", on_delete=models.CASCADE, related_name="%(class)ss"
    )

    objects = TenantManager()

    def save(self, *args, **kwargs):
        if not hasattr(self, "academy_id") or self.academy_id is None:
            academy_id = get_current_academy_id()
            if academy_id:
                self.academy_id = academy_id
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
