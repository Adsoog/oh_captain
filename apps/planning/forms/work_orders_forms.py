from django import forms
from apps.planning.models.workorder_models import WorkOrder


class WorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = ['proforma', 'equipments', 'assets', 'planned_date', 'status']
        widgets = {
            # Usamos un widget de tipo datetime-local para el campo planned_date
            'planned_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class WorkOrderEquipmentForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = ['equipments']
        widgets = {
            'equipments': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


class WorkOrderAssetForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = ['assets']
        widgets = {
            'assets': forms.Select(attrs={'class': 'form-control'}),
        }


class WorkOrderWorkerForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = ['workers']
        widgets = {
            'workers': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
