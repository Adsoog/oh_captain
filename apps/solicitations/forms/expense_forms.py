from django import  forms
from apps.solicitations.models.expenses_models import ExpenseItem

class ExpenseItemForm(forms.ModelForm):
    class Meta:
        model = ExpenseItem
        fields = [
            "date",
            "ruc_or_dni",
            "description",
            "doc_type",
            "doc",
            "cost_center",
            "amount",
            "file",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "ruc_or_dni": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "doc_type": forms.Select(attrs={"class": "form-control"}),
            "document": forms.TextInput(attrs={"class": "form-control"}),
            "cost_center": forms.Select(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
            "file": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
        }