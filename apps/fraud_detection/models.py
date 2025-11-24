# apps/fraud_detection/models.py
from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model

# Import correct du modèle User personnalisé
User = get_user_model()

class MLModelVersion(models.Model):
    name = models.CharField(max_length=50, unique=True)
    version = models.CharField(max_length=20)
    file = models.FileField(
        upload_to='ml_models/',
        validators=[FileExtensionValidator(['pkl', 'joblib'])],
        help_text=".pkl ou .joblib"
    )
    accuracy = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Modèle ML"

    def __str__(self):
        return f"{self.name} v{self.version} {'(ACTIF)' if self.is_active else ''}"

    def save(self, *args, **kwargs):
        if self.is_active:
            MLModelVersion.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class UserBehaviorLog(models.Model):
    EVENT_CHOICES = [
        ('login', 'Connexion'),
        ('report', 'Signalement'),
        ('high_risk', 'Risque élevé détecté'),
        ('blocked', 'Numéro bloqué'),
    ]

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='behavior_logs'
    )
    event_type = models.CharField(max_length=20, choices=EVENT_CHOICES)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Journal comportement"

    def __str__(self):
        return f"{self.user} - {self.get_event_type_display()} - {self.timestamp.strftime('%d/%m %H:%M')}"