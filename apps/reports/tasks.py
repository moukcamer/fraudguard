# apps/reports/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from apps.accounts.utils import send_sms_2fa

@shared_task
def send_report_notification(report_id):
    from .models import FraudReport
    report = FraudReport.objects.get(id=report_id)
    
    # Email to admin
    send_mail(
        subject=f"Nouveau signalement: {report.get_report_type_display()}",
        message=f"""
        Utilisateur: {report.reporter}
        Type: {report.get_report_type_display()}
        Cible: {report.target_phone or report.target_account}
        Date: {report.created_at.strftime('%d/%m/%Y %H:%M')}
        Lien: https://fraudguard.cm/admin/reports/fraudreport/{report.id}/change/
        """,
        from_email='reports@fraudguard.cm',
        recipient_list=['admin@fraudguard.cm'],
    )

    # SMS to reporter (confirmation)
    send_sms_2fa(
        phone=report.reporter.phone,
        code=f"Signalement #{report.id[:8]} reçu. Merci !"
    )