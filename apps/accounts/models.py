# apps/accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone


class User(AbstractUser):
    """
    Modèle utilisateur personnalisé FraudGuard (Cameroun)
    """
    # Validation numéro camerounais +237
    phone_regex = RegexValidator(
        regex=r'^\+237[6-9]\d{8}$',
        message="Format requis : +237XXXXXXXXX (ex: +237699123456)"
    )

    phone = models.CharField(
        max_length=13,
        unique=True,
        validators=[phone_regex],
        blank=True,
        null=True,
        help_text="Numéro camerounais"
    )
    is_verified = models.BooleanField(default=False)
    language = models.CharField(
        max_length=5,
        choices=[('fr', 'Français'), ('en', 'English')],
        default='fr'
    )
    currency = models.CharField(max_length=3, default='XAF')

    # Sécurité : évite les erreurs si date_joined est manquant
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username or self.phone or self.email