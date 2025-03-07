from django import forms
from django.forms import modelformset_factory
from apps.commercial.models.proforma_models import Service, Equipment


class EquipmentAddForm(forms.ModelForm):
    service = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Equipment
        fields = ["quoted_instrument", "service", "service_place"]


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = '__all__'
        exclude = ['proforma', 'instrument']

EquipmentFormSet = modelformset_factory(Equipment, form=EquipmentForm, extra=0)
