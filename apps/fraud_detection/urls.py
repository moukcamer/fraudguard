# apps/fraud_detection/urls.py


from django.urls import path
from .views import RiskScoreAPIView   # ← LA SEULE VUE QUI EXISTE

urlpatterns = [
    path('risk/', RiskScoreAPIView.as_view(), name='risk_score'),
]