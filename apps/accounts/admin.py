# apps/accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username', 'email', 'phone', 'is_verified', 'is_staff', 'date_joined']
    list_filter = ['is_verified', 'is_staff', 'date_joined']
    search_fields = ['username', 'email', 'phone']
    actions = ['mark_verified', 'mark_unverified']   # CORRIGÉ

    fieldsets = UserAdmin.fieldsets + (
        ('Infos Cameroun', {'fields': ('phone', 'is_verified', 'language', 'currency')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Infos Cameroun', {'fields': ('phone', 'language')}),
    )

    def mark_verified(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f"{updated} utilisateur(s) marqué(s) comme vérifié(s).")
    mark_verified.short_description = "Marquer comme vérifié"

    def mark_unverified(self, request, queryset):
        updated = queryset.update(is_verified=False)
        self.message_user(request, f"{updated} utilisateur(s) marqué(s) comme non vérifié(s).")
    mark_unverified.short_description = "Marquer comme non vérifié"