# apps/analytics/utils.py
import json
from django.conf import settings

def get_cameroon_geojson():
    path = settings.BASE_DIR / 'static' / 'analytics' / 'geo' / 'cameroon_regions.json'
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return None