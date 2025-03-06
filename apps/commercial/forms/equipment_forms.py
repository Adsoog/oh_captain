from django import forms
from apps.commercial.models.proforma_models import Service, Equipment


class EquipmentAddForm(forms.ModelForm):
    service = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = Equipment
        fields = ["instrument", "service", "service_place"]