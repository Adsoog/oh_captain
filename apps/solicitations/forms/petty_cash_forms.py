from django import forms
from apps.solicitations.models.petty_cash_models import PettyCash


class PettyCashForm(forms.ModelForm):
    class Meta:
        model = PettyCash
        fields = ['details']
        widgets = {
            'details': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Ingrese detalles para caja chica...'})
        }

