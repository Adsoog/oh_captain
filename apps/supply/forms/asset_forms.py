from django import forms
from ..models.asset_models import Asset, AssetRequest


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = [
            'name',
            'asset_type',
            'serial_number',
            'location',
            'status',
            'assigned_to',
            'acquisition_date',
            'quantity_available',
            'notes',
        ]
        widgets = {
            'acquisition_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class AssetRequestForm(forms.ModelForm):
    asset = forms.ModelChoiceField(
        queryset=Asset.objects.filter(status=Asset.Status.AVAILABLE),  # Solo activos disponibles
        label="Selecciona el activo",
        widget=forms.Select(attrs={'class': 'form-input p-2 w-full'})
    )

    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        label="Cantidad",
        widget=forms.NumberInput(attrs={'class': 'form-input p-2 w-full'})
    )

    class Meta:
        model = AssetRequest
        fields = ['asset', 'quantity', 'approved_by']
