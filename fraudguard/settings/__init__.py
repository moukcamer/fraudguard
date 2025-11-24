# fraudguard/settings/__init__.py
from .base import *

# Load environment-specific settings
import os
env = os.getenv('DJANGO_ENV', 'development')

if env == 'production':
    from .production import *
elif env == 'development':
    from .development import *