from apps.solicitations.models.solicitation_models import Solicitation
from django import forms


class SolicitationForm(forms.ModelForm):
    class Meta:
        model = Solicitation
        fields = [
            'correlative', 'requested_at', 'period', 'reason', 'employee',
            'area', 'department', 'oti', 'client', 'solicitation_type'
        ]
        widgets = {
            'requested_at': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reason': forms.TextInput(attrs={'class': 'form-control'}),
            'correlative': forms.TextInput(attrs={'class': 'form-control'}),
            'oti': forms.TextInput(attrs={'class': 'form-control'}),
            'client': forms.TextInput(attrs={'class': 'form-control'}),
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'area': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'period': forms.Select(attrs={'class': 'form-control'}),
            'solicitation_type': forms.Select(attrs={'class': 'form-control'}),
        }
