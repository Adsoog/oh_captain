from django import forms
from apps.commercial.models.proforma_models import Proforma


class ProformaForm(forms.ModelForm):
    class Meta:
        model = Proforma
        fields = ['client', 'request_date', 'proforma_date', 'offer_validity', 'certificate_address',
                  'certificate_owner', 'service_type', 'service_address']
