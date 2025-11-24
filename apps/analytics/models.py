# apps/analytics/models.py
from django.db import models
from django.utils import timezone


class FraudTrend(models.Model):
    """
    Statistiques quotidiennes de fraude (remplies par une tâche Celery)
    """
    date = models.DateField(default=timezone.now, unique=True)
    total_reports = models.PositiveIntegerField(default=0)
    fraud_detected = models.PositiveIntegerField(default=0)
    safe_reports = models.PositiveIntegerField(default=0)
    avg_risk_score = models.FloatField(default=0.0)

    class Meta:
        ordering = ['-date']
        verbose_name = "Tendance Fraude"
        verbose_name_plural = "Tendances Fraude"

    def __str__(self):
        return f"{self.date} – {self.fraud_detected} fraudes détectées"