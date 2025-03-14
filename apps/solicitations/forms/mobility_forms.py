from django import forms
from apps.solicitations.models.mobility_models import MobilitySheet, MobilityItem


class MobilitySheetForm(forms.ModelForm):
    class Meta:
        model = MobilitySheet
        fields = [
            'issue_date',
        ]
        widgets = {
            'issue_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Seleccione la fecha de emisión',
            }),
        }


class MobilityItemForm(forms.ModelForm):
    class Meta:
        model = MobilityItem
        fields = [
            'expense_date',
            'reason',
            'route',
            'transport',
            'daily_amount',
            'approver_signature'
        ]
        widgets = {
            'expense_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'border border-gray-300 rounded-md px-2 py-1 w-full',
                }
            ),
            'reason': forms.TextInput(attrs={
                'class': 'border border-gray-300 rounded-md px-2 py-1 w-full',
                'placeholder': 'Motivo del gasto',
            }),
            'route': forms.TextInput(attrs={
                'class': 'border border-gray-300 rounded-md px-2 py-1 w-full',
                'placeholder': 'Ruta cubierta',
            }),
            'transport_mode': forms.TextInput(attrs={
                'class': 'border border-gray-300 rounded-md px-2 py-1 w-full',
                'placeholder': 'Medio de transporte',
            }),
            'daily_amount': forms.NumberInput(attrs={
                'class': 'border border-gray-300 rounded-md px-2 py-1 w-full',
                'placeholder': 'Monto gastado',
            }),
        }
