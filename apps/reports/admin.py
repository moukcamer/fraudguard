# apps/reports/admin.py
from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'status', 'risk_score', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'phone_number']
    actions = ['mark_as_fraud', 'mark_as_safe']   # ← CORRECT : liste de strings

    def mark_as_fraud(self, request, queryset):
        queryset.update(status='fraud')
        self.message_user(request, f"{queryset.count()} rapport(s) marqué(s) comme fraude.")
    mark_as_fraud.short_description = "Marquer comme fraude"

    def mark_as_safe(self, request, queryset):
        queryset.update(status='safe')
        self.message_user(request, f"{queryset.count()} rapport(s) marqué(s) comme sûr.")
    mark_as_safe.short_description = "Marquer comme sûr"