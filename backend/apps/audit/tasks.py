from celery import shared_task

from .models import AuditLog


@shared_task
def write_audit_log(
    actor_id=None,
    academy_id=None,
    action="",
    entity_type="",
    entity_id="",
    old_value=None,
    new_value=None,
    ip_address=None,
    user_agent=None,
    metadata=None,
):
    AuditLog.objects.create(
        actor_id=actor_id,
        academy_id=academy_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        old_value=old_value or None,
        new_value=new_value or None,
        ip_address=ip_address or None,
        user_agent=user_agent or "",
        metadata=metadata or {},
    )
