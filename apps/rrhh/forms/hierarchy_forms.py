from django import forms
from apps.rrhh.models.employee_models import Employee


class EmployeeHierarchyForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['parent']
