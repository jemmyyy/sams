from django.core.cache import cache
from apps.common.thread_local import get_current_academy_id

class TenantSafeCache:
    """
    Utility for academy-scoped caching.
    """
    @staticmethod
    def _make_key(key):
        academy_id = get_current_academy_id()
        if not academy_id:
            return f"global:{key}"
        return f"academy:{academy_id}:{key}"

    @classmethod
    def set(cls, key, value, timeout=None):
        return cache.set(cls._make_key(key), value, timeout)

    @classmethod
    def get(cls, key, default=None):
        return cache.get(cls._make_key(key), default)

    @classmethod
    def delete(cls, key):
        return cache.delete(cls._make_key(key))
