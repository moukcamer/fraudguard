# apps/fraud_detection/tasks.py
from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()

# On enlève complètement FraudAlert – il n’existe pas et n’est pas nécessaire


@shared_task
def log_high_risk_behavior(user_id, description):
    """
    Log un comportement suspect (ex: SMS à haut risque)
    """
    from .models import UserBehaviorLog
    try:
        user = User.objects.get(id=user_id)
        UserBehaviorLog.objects.create(
            user=user,
            event_type='high_risk',
            description=description,
            ip_address="N/A"  # Tu pourras ajouter la vraie IP plus tard
        )
    except User.DoesNotExist:
        pass


@shared_task
def send_alert_email(user_id, risk_score, message_text):
    """
    Envoi d'email d'alerte (optionnel plus tard)
    """
    try:
        user = User.objects.get(id=user_id)
        subject = f"⚠️ Fraude détectée – Score: {risk_score}%"
        message = f"""
        Bonjour {user.username},

        Un message suspect a été détecté sur votre compte FraudGuard :
        
        Message : {message_text[:200]}...
        Risque : {risk_score}% (ÉLEVÉ)

        Protégez-vous immédiatement :
        - Ne cliquez sur aucun lien
        - Ne partagez jamais votre code secret
        - Bloquez l’expéditeur

        L’équipe FraudGuard
        """
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )
    except User.DoesNotExist:
        pass