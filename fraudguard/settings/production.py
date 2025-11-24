# fraudguard/settings/production.py
from .base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

DEBUG = False

# Hosts
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'fraudguard.cm,www.fraudguard.cm,api.fraudguard.cm').split(',')

# Secret Key
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# Database (PostgreSQL)
DATABASES['default'].update({
    'NAME': os.getenv('POSTGRES_DB'),
    'USER': os.getenv('POSTGRES_USER'),
    'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
    'HOST': os.getenv('POSTGRES_HOST'),
    'PORT': os.getenv('POSTGRES_PORT', '5432'),
})

# Static files
STATIC_ROOT = '/var/www/fraudguard/static/'
MEDIA_ROOT = '/var/www/fraudguard/media/'

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Email (Use real SMTP)
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# CORS (Restrict in prod)
CORS_ALLOWED_ORIGINS = [
    "https://fraudguard.cm",
    "https://www.fraudguard.cm",
    "https://app.fraudguard.cm",
]

# Sentry (Error tracking)
sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.2,
    send_default_pii=True
)

# Logging to file
import os
os.makedirs(BASE_DIR / 'logs', exist_ok=True)