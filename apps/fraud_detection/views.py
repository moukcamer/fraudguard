# apps/fraud_detection/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .ml_service import predict_fraud_risk

class RiskScoreAPIView(APIView):
        """
    Endpoint public ou authentifié pour calculer le risque d'un SMS
    POST /api/fraud/risk/
    {
        "text": "Orange Money gagnant 500000 XAF, cliquez ici"
    }
    """

permission_classes = [AllowAny]

def post(self, request):
        text = request.data.get('text', '').strip()

        if not text:
            return Response(
                {"error": "Le champ 'text' est requis"},
                status=status.HTTP_400_BAD_REQUEST
            )

        risk_score = predict_fraud_risk(text)
        is_fraud = risk_score > 70

        response_data = {
            "risk_score": round(risk_score, 2),
            "is_fraud": is_fraud,
            "level": "ÉLEVÉ" if is_fraud else "FAIBLE",
            "advice": "Bloquez l’expéditeur immédiatement" if is_fraud else "Message probablement sûr"
        }

        # AUCUN ENVOI D'ALERTE → AUCUNE CONNEXION REDIS → AUCUNE ERREUR

        return Response(response_data)