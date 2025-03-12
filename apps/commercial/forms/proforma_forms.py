from django import forms
from apps.commercial.models.proforma_models import Proforma


class ProformaForm(forms.ModelForm):
    class Meta:
        model = Proforma
        fields = ['client', 'branch', 'request_date', 'proforma_date', 'offer_validity',
                  'certificate_address', 'certificate_owner', 'service_type', 'service_address']
        widgets = {
            'client': forms.Select(attrs={
                'placeholder': 'Seleccione un cliente',
            }),
            'branch': forms.Select(attrs={
                'placeholder': 'Selecciona una sede',
            }),
            'request_date': forms.TextInput(attrs={
                'placeholder': 'DD/MM/YYYY'
            }),
            'proforma_date': forms.TextInput(attrs={
                'placeholder': 'DD/MM/YYYY'
            }),
            'offer_validity': forms.NumberInput(attrs={
                'placeholder': 'Cantidad de días'
            }),
            'certificate_address': forms.TextInput(attrs={
                'placeholder': 'Dirección del certificado'
            }),
            'certificate_owner': forms.TextInput(attrs={
                'placeholder': 'Razón social del certificado'
            }),
            'service_type': forms.Select(attrs={
                'placeholder': 'Seleccione un tipo de servicio',
            }),
            'service_address': forms.TextInput(attrs={
                'placeholder': 'Dirección del servicio'
            }),
        }
