from django import forms
from apps.commercial.models.proforma_models import Proforma, Client, Branch
from dynamic_forms import DynamicField, DynamicFormMixin


class ProformaForm(DynamicFormMixin, forms.ModelForm):

    def branch_choices(form):
        client = form['client'].value()
        if client:
            return Branch.objects.filter(client=client)
        return Branch.objects.none()

    def initial_branch(form):
        client = form['client'].value()
        if client:
            return Branch.objects.filter(client=client).first()
        return None

    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        initial=Client.objects.first()
    )
    branch = DynamicField(
        forms.ModelChoiceField,
        queryset=branch_choices,
        initial=initial_branch
    )

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
