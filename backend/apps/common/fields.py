import base64
import hashlib

from django.conf import settings
from django.db import models
from cryptography.fernet import Fernet


def _get_fernet():
    key = getattr(settings, "FIELD_ENCRYPTION_KEY", None)
    if not key:
        raw = getattr(settings, "SECRET_KEY", "").encode()
        key = base64.urlsafe_b64encode(hashlib.sha256(raw).digest())
    if isinstance(key, str):
        key = key.encode()
    return Fernet(key)


class EncryptedTextField(models.TextField):
    def get_prep_value(self, value):
        if value is None or value == "":
            return value
        f = _get_fernet()
        return f.encrypt(value.encode()).decode()

    def from_db_value(self, value, expression, connection):
        if value is None or value == "":
            return value
        try:
            f = _get_fernet()
            return f.decrypt(value.encode()).decode()
        except Exception:
            return value
