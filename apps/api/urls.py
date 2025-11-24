# apps/api/urls.py
from django.urls import path, include
from apps.fraud_detection.views import RiskScoreAPIView

urlpatterns = [
    # Endpoint principal de détection de fraude
    path('fraud/risk/', RiskScoreAPIView.as_view(), name='risk_score'),
    
    # Autres endpoints
    path('reports/', include('apps.reports.urls')),
    path('analytics/', include('apps.analytics.urls')),
]