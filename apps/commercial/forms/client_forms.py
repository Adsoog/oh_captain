from django.conf import settings
from django.core.validators import RegexValidator
from django import forms
from django.contrib.auth import get_user_model
from apps.commercial.models.client_models import Client, Branch


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'business_name',
            'tax_id',
            'address',
            'department',
            'economic_activity',
            'workers_number',
            'billing_type',
            'accounting_type',
            'foreign_trade',
            'company_type',
            'payment_method',
        ]


class ClientLookupForm(forms.Form):
    tax_id = forms.CharField(
        max_length=11,
        min_length=11,
        label="RUC",
        validators=[
            RegexValidator(r'^\d{11}$', message="El RUC debe contener exactamente 11 dígitos numéricos.")
        ],
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500',
            'placeholder': 'Ingrese el RUC',
            'min': '10000000000',  # Evita números menores de 11 dígitos
            'max': '99999999999',  # Evita números mayores de 11 dígitos
            'pattern': '[0-9]{11}',  # HTML5: Asegura que sean exactamente 11 números
            'title': 'Debe ingresar exactamente 11 dígitos numéricos'
        })
    )


class BranchForm(forms.ModelForm):
    sales_advisor = forms.ModelChoiceField(
        queryset=get_user_model().objects.filter(groups__name="DEP_COMERCIAL"),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        required=False,
        label="Asesor de Ventas"
    )

    class Meta:
        model = Branch
        fields = ['name', 'address', 'department', 'is_headquarters', 'sales_advisor']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la sede'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Dirección', 'rows': 3}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Departamento'}),
            'is_headquarters': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar los usuarios por el grupo 'DEP_COMERCIAL'
        self.fields['sales_advisor'].queryset = get_user_model().objects.filter(groups__name="DEP_COMERCIAL")