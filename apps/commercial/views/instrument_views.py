from apps.commercial.utils import process_instruments_excel, export_instruments_to_excel
from django.views.generic import ListView
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from apps.commercial.models.instrument_models import Instrument


class InstrumentListView(ListView):
    model = Instrument
    template_name = 'commercial/instrument/instruments_list.html'
    context_object_name = 'instruments'


def instruments_list(request):
    instruments = Instrument.objects.all()
    return render(request, 'commercial/instrument/instruments_list.html', {'instruments': instruments})


def instrument_detail(request, id):
    instrument = get_object_or_404(Instrument, id=id)
    return render(request, 'commercial/instrument/instrument_detail.html', {'instrument': instrument})


def upload_instruments_list(request):
    if request.method == 'POST' and request.FILES.get('file'):
        excel_file = request.FILES['file']
        result = process_instruments_excel(excel_file)
        if 'Error' in result:
            return HttpResponseBadRequest(result)
        return redirect('instruments_list')


def download_instruments_list(request):
    excel_file = export_instruments_to_excel()
    response = HttpResponse(excel_file.read(),
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="instruments_report.xlsx"'
    return response
