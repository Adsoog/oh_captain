from django import forms
from apps.commercial.models.instrument_models import Instrument

class InstrumentForm(forms.ModelForm):
    class Meta:
        model = Instrument
        fields = '__all__'
