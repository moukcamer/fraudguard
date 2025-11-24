# apps/fraud_detection/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import MLModelVersion

@admin.register(MLModelVersion)
class MLModelVersionAdmin(admin.ModelAdmin):
    list_display = ['name', 'version', 'accuracy', 'is_active', 'created_at', 'file_link']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'version']
    actions = ['activate_model']   # CORRIGÉ

    def file_link(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">Télécharger</a>', obj.file.url)
        return "-"
    file_link.short_description = "Fichier"

    def activate_model(self, request, queryset):
        MLModelVersion.objects.update(is_active=False)
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} modèle(s) activé(s).")
    activate_model.short_description = "Activer le(s) modèle(s)"