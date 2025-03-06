from django.views.generic import ListView
from django.shortcuts import render
from apps.commercial.models.instrument_models import Instrument

class InstrumentListView(ListView):
    model = Instrument
    template_name = 'commercial/instrument/instruments_list.html'
    context_object_name = 'instruments'

def instruments_list(request):
    instruments = Instrument.objects.all()
    return render(request, 'commercial/instrument/instruments_list.html', {'instruments': instruments})

