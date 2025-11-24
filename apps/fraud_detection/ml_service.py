# apps/fraud_detection/ml_service.py
import joblib
import os
import re
from django.conf import settings
from pathlib import Path

# Mots-clés frauduleux très forts au Cameroun
FRAUD_KEYWORDS = [
    'orange money', 'gagnant', '500000', 'cliquez', 'urgent', 'cadeau',
    'mobile money', 'code secret', 'envoyez', 'gratuit', 'mtn momo',
    'votre compte bloqué', 'vérifiez', 'lien', 'cliquez ici', 'xof'
]

def predict_fraud_risk(text: str) -> float:
    """
    Retourne un score de 0 à 100 sans PyTorch ni Hugging Face
    Très efficace sur les fraudes SMS camerounaises
    """
    if not text:
        return 0.0

    text = text.lower()
    score = 0.0

    # 1. Comptage mots-clés (très fiable au Cameroun)
    matched = sum(1 for word in FRAUD_KEYWORDS if word in text)
    score += matched * 25

    # 2. Présence de lien ou numéro
    if re.search(r'http[s]?://|bit\.ly|tinyurl|\d{8,}', text):
        score += 30

    # 3. Urgence
    if any(word in text for word in ['urgent', 'immédiat', 'aujourd’hui', 'maintenant']):
        score += 20

    # 4. Demande d’argent ou code
    if any(word in text for word in ['envoyez', 'transférez', 'code', 'pin']):
        score += 25

    return min(round(score, 2), 100.0)