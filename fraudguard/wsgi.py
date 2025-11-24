# fraudguard/wsgi.py
import os
from django.core.wsgi import get_wsgi_application

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fraudguard.settings')

# Get WSGI application
application = get_wsgi_application()

# Optional: Add WhiteNoise for static files in production
try:
    from whitenoise import WhiteNoise
    application = WhiteNoise(application, root='staticfiles')
except ImportError:
    pass  # WhiteNoise not installed in dev