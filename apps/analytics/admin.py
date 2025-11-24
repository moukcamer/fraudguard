# apps/analytics/admin.py
from django.contrib import admin
from .models import FraudTrend

@admin.register(FraudTrend)
class FraudTrendAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_reports', 'fraud_detected', 'safe_reports', 'avg_risk_score']
    list_filter = ['date']
    readonly_fields = ['date', 'total_reports', 'fraud_detected', 'safe_reports', 'avg_risk_score']
    search_fields = ['date']
    # Pas d'actions → on laisse vide ou on met une liste vide
    actions = []   # CORRIGÉ et propre