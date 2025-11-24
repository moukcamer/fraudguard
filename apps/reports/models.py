# apps/reports/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Report(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('fraud', 'Fraude détectée'),
        ('safe', 'Sûr'),
        ('review', 'En révision'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    description = models.TextField("Description du message suspect")
    phone_number = models.CharField(max_length=13, blank=True, help_text="+237XXXXXXXXX")
    evidence = models.FileField(upload_to='reports/evidence/', blank=True, null=True)
    risk_score = models.FloatField(default=0.0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Rapport"
        verbose_name_plural = "Rapports"

    def __str__(self):
        return f"Rapport #{self.id} – {self.user} – {self.status}"