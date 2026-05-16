from .base import *

DEBUG = False

# --- Security ---
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# --- Hosts ---
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# --- CORS ---
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")

# --- Database ---
DATABASES["default"]["CONN_MAX_AGE"] = 600
DATABASES["default"]["OPTIONS"] = {
    "connect_timeout": 10,
}

# --- Email ---
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="smtp.mailgun.org")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")

# --- Sentry ---
SENTRY_DSN = env("SENTRY_DSN", default="")
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.celery import CeleryIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration(), CeleryIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=False,
    )

# --- Static files ---
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

# --- Cache ---
CACHES["default"]["OPTIONS"]["CLIENT_CLASS"] = "django_redis.client.DefaultClient"
CACHES["default"]["TIMEOUT"] = 300

# --- Object Storage (MinIO / S3) ---
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID", default="")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY", default="")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME", default="sams-media")
AWS_S3_ENDPOINT_URL = env("AWS_S3_ENDPOINT_URL", default="")
AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME", default="us-east-1")
AWS_DEFAULT_ACL = "private"
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_QUERYSTRING_EXPIRE = 3600

if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
        },
    }

# --- Logging ---
LOGGING["root"]["level"] = "WARNING"
LOGGING["handlers"]["file"]["level"] = "WARNING"
