from django import forms
from ..models.asset_models import Asset

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
            'notes'
        ]
        widgets = {
            'acquisition_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
