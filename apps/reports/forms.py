# apps/reports/forms.py
from django import forms
from .models import FraudReport

class FraudReportForm(forms.ModelForm):
    class Meta:
        model = FraudReport
        fields = ['report_type', 'target_phone', 'target_account', 'description', 'evidence']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Ex: J\'ai reçu un SMS me demandant d\'envoyer 5000 FCFA pour débloquer un prix...'}),
            'target_phone': forms.TextInput(attrs={'placeholder': '+237XXXXXXXXX'}),
        }

    def clean_evidence(self):
        file = self.cleaned_data.get('evidence')
        if file:
            if file.size > 10 * 1024 * 1024:  # 10MB
                raise forms.ValidationError("Le fichier est trop grand (max 10 Mo).")
            if not file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.pdf', '.txt')):
                raise forms.ValidationError("Format non autorisé. Utilisez PNG, JPG, PDF ou TXT.")
        return file