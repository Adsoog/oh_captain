from django import  forms
from apps.solicitations.models.expenses_models import Expenses

class ExpensesForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = ['details']
        widgets = {
            'details': forms.Textarea(attrs={'class': 'form-control', 'rows': 4,
                                             'placeholder': 'Ingrese detalles para entregas por rendir...'})
        }