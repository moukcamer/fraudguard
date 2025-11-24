# apps/api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

class APIRootView(APIView):
    def get(self, request):
        return Response({
            "name": "FraudGuard API",
            "version": "v1",
            "docs": {
                "swagger": reverse('api:swagger-ui', request=request),
                "redoc": reverse('api:redoc', request=request),
            },
            "endpoints": {
                "fraud_detection": reverse('api:v1-fraud-risk', request=request),
                "reports": reverse('api:report-list', request=request),
                "analytics": reverse('api:analytics-stats', request=request),
                "auth": reverse('api:v1-auth-login', request=request),
            },
            "country": "CM",
            "timezone": "Africa/Douala",
            "support": "support@fraudguard.cm"
        })