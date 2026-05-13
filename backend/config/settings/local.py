from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

# In local, we might want to use console email backend or similar
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS += ["django_extensions"]
