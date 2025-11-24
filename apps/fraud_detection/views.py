# apps/fraud_detection/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

from .ml_service import predict_fraud_risk


class RiskScoreAPIView(APIView):
    """
    Endpoint public ou authentifié pour calculer le risque d'un SMS
    POST /api/fraud/risk/
    {
        "text": "Orange Money gagnant 500000 XAF, cliquez ici"
    }
    """
    permission_classes = [AllowAny]  # Tu peux mettre IsAuthenticated si tu veux

    def post(self, request):
        text = request.data.get('text', '').strip()

        if not text:
            return Response(
                {"error": "Le champ 'text' est requis"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calcul du risque
        risk_score = predict_fraud_risk(text)
        is_fraud = risk_score > 70

        response_data = {
            "risk_score": round(risk_score, 2),
            "is_fraud": is_fraud,
            "level": "ÉLEVÉ" if is_fraud else "FAIBLE",
            "advice": "Bloquez l’expéditeur immédiatement" if is_fraud else "Message probablement sûr"
        }

        # Envoi d'une alerte WebSocket en temps réel si fraude détectée
        if is_fraud:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "fraud_alerts",
                {
                    "type": "fraud_alert",
                    "message": {
                        "user": request.user.username if request.user.is_authenticated else "Anonyme",
                        "phone": getattr(request.user, 'phone', 'Inconnu') if request.user.is_authenticated else "N/A",
                        "text": text[:100] + "..." if len(text) > 100 else text,
                        "risk": round(risk_score, 1),
                        "timestamp": __import__('time').strftime("%H:%M:%S")
                    }
                }
            )

        return Response(response_data, status=status.HTTP_200_OK)