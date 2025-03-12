from apps.solicitations.models.solicitation_models import (
    ExitTicket,
    Expenses,
    PettyCash,
    MobilitySheet,
    PerdiemRequest,
    Solicitation,
)
from django import forms


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
            'client': forms.TextInput(attrs={'class': 'form-control'}),
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'area': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'solicitation_type': forms.Select(attrs={'class': 'form-control'}),
        }


class ExitTicketForm(forms.ModelForm):
    class Meta:
        model = ExitTicket
        fields = ['details']
        widgets = {
            'details': forms.Textarea(attrs={'class': 'form-control', 'rows': 4,
                                             'placeholder': 'Ingrese detalles de la papeleta de salida...'})
        }


class ExpensesForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = ['details']
        widgets = {
            'details': forms.Textarea(attrs={'class': 'form-control', 'rows': 4,
                                             'placeholder': 'Ingrese detalles para entregas por rendir...'})
        }


class PettyCashForm(forms.ModelForm):
    class Meta:
        model = PettyCash
        fields = ['details']
        widgets = {
            'details': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Ingrese detalles para caja chica...'})
        }


class MobilitySheetForm(forms.ModelForm):
    class Meta:
        model = MobilitySheet
        fields = ['details']
        widgets = {
            'details': forms.Textarea(attrs={'class': 'form-control', 'rows': 4,
                                             'placeholder': 'Ingrese detalles para planilla de movilidad...'})
        }


class PerdiemRequestForm(forms.ModelForm):
    class Meta:
        model = PerdiemRequest
        fields = ['details']
        widgets = {
            'details': forms.Textarea(attrs={'class': 'form-control', 'rows': 4,
                                             'placeholder': 'Ingrese detalles para solicitud de viáticos...'})
        }
