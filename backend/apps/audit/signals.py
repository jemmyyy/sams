import json

from django.db.models.signals import post_delete, post_save

from .tasks import write_audit_log


def _get_changed_fields(instance):
    """Return dict of changed fields with old/new values."""
    if not instance.pk:
        return None
    try:
        old = type(instance).all_objects.get(pk=instance.pk)
    except type(instance).DoesNotExist:
        return None
    changes = {}
    for field in instance._meta.fields:
        field_name = field.name
        if field_name in ("created_at", "updated_at", "deleted_at"):
            continue
        old_val = getattr(old, field_name, None)
        new_val = getattr(instance, field_name, None)
        if old_val != new_val:
            changes[field_name] = {"old": str(old_val), "new": str(new_val)}
    return changes or None


def _serialize_instance(instance):
    data = {}
    for field in instance._meta.fields:
        val = getattr(instance, field.name)
        if hasattr(val, "pk"):
            data[field.name] = str(val.pk)
        else:
            try:
                json.dumps(val)
                data[field.name] = val
            except (TypeError, ValueError):
                data[field.name] = str(val)
    return data


def _get_academy_id(instance):
    if hasattr(instance, "academy_id"):
        return str(instance.academy_id)
    return None


def post_save_audit(sender, instance, created, **kwargs):
    if sender.__name__ == "AuditLog" or sender.__name__ == "Migration":
        return
    actor_id = _get_actor_from_thread()
    academy_id = _get_academy_id(instance)
    if created:
        write_audit_log.delay(
            actor_id=actor_id,
            academy_id=academy_id,
            action="create",
            entity_type=sender.__name__,
            entity_id=str(instance.pk),
            new_value=_serialize_instance(instance),
        )
    else:
        changes = _get_changed_fields(instance)
        if changes:
            write_audit_log.delay(
                actor_id=actor_id,
                academy_id=academy_id,
                action="update",
                entity_type=sender.__name__,
                entity_id=str(instance.pk),
                old_value={k: v["old"] for k, v in changes.items()},
                new_value={k: v["new"] for k, v in changes.items()},
            )


def post_delete_audit(sender, instance, **kwargs):
    if sender.__name__ == "AuditLog" or sender.__name__ == "Migration":
        return
    actor_id = _get_actor_from_thread()
    academy_id = _get_academy_id(instance)
    write_audit_log.delay(
        actor_id=actor_id,
        academy_id=academy_id,
        action="delete",
        entity_type=sender.__name__,
        entity_id=str(instance.pk),
        old_value=_serialize_instance(instance),
    )


def _get_actor_from_thread():
    """Extract current user ID from thread-local or request context."""
    import threading

    request = getattr(threading.current_thread(), "request", None)
    if request and hasattr(request, "user") and request.user.is_authenticated:
        return str(request.user.id)
    return None


def _should_audit(sender):
    """Only audit models that have an academy FK (tenant-aware models)."""
    return (
        hasattr(sender, "_meta")
        and any(f.name == "academy" for f in sender._meta.fields)
        and sender.__name__ != "AuditLog"
    )


def _post_save_handler(sender, instance, created, **kwargs):
    if not _should_audit(sender):
        return
    post_save_audit(sender, instance, created, **kwargs)


def _post_delete_handler(sender, instance, **kwargs):
    if not _should_audit(sender):
        return
    post_delete_audit(sender, instance, **kwargs)


post_save.connect(_post_save_handler, dispatch_uid="audit_post_save")
post_delete.connect(_post_delete_handler, dispatch_uid="audit_post_delete")
