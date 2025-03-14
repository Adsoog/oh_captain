from apps.solicitations.models.solicitation_models import Solicitation
from django import forms


class SolicitationTypeForm(forms.ModelForm):
    class Meta:
        model = Solicitation
        fields = [
            'solicitation_type',
        ]
        widgets = {
            'solicitation_type': forms.Select(attrs={'class': 'form-control'}),
        }

class SolicitationForm(forms.ModelForm):
    class Meta:
        model = Solicitation
        fields = [
            'requested_at', 'reason', 'employee',
            'area', 'department', 'work_order', 'client', 'solicitation_type'
        ]
        widgets = {
            'requested_at': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reason': forms.TextInput(attrs={'class': 'form-control'}),
            'work_order': forms.Select(attrs={'class': 'form-control'}),
            'client': forms.Select(attrs={'class': 'form-control'}),
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'area': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'solicitation_type': forms.Select(attrs={'class': 'form-control'}),
        }

