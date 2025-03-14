from django import forms
from apps.solicitations.models.exit_ticket_models import ExitTicket

class ExitTicketForm(forms.ModelForm):
    class Meta:
        model = ExitTicket
        fields = ['details']
        widgets = {
            'details': forms.Textarea(attrs={'class': 'form-control', 'rows': 4,
                                             'placeholder': 'Ingrese detalles de la papeleta de salida...'})
        }