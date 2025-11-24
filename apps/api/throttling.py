# apps/api/throttling.py
from rest_framework.throttling import UserRateThrottle

class FraudCheckThrottle(UserRateThrottle):
    rate = '5/minute'  # Prevent abuse