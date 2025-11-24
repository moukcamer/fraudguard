# apps/reports/views.py
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Report  # ← CORRIGÉ : c’est Report, pas FraudReport
from .serializers import ReportSerializer
from apps.fraud_detection.ml_service import predict_fraud_risk
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json


class ReportCreateView(generics.CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Analyse IA du texte
        text = serializer.validated_data.get('description', '')
        risk_score = predict_fraud_risk(text)
        is_fraud = risk_score > 70

        # Sauvegarde avec score
        report = serializer.save(
            user=self.request.user,
            risk_score=risk_score,
            status='fraud' if is_fraud else 'safe'
        )

        # Alerte WebSocket si fraude
        if is_fraud:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "fraud_alerts",
                {
                    "type": "fraud_alert",
                    "message": {
                        "user": self.request.user.username,
                        "phone": report.phone_number or "Inconnu",
                        "text": text[:100] + "..." if len(text) > 100 else text,
                        "risk": round(risk_score, 1),
                        "timestamp": __import__('time').strftime("%H:%M:%S")
                    }
                }
            )

        return report


class ReportListView(generics.ListAPIView):
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Report.objects.filter(user=self.request.user).order_by('-created_at')