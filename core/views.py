from django.db.models import Q
from django.shortcuts import render
from apps.commercial.models.proforma_models import Proforma, Client
from apps.supply.models.asset_models import Asset


def generic_search(request):
    model_name = request.GET.get('model')
    query = request.GET.get('q', '').strip()

    if model_name == 'client':
        clients = Client.objects.filter(business_name__icontains=query)[:10]
        return render(request, 'core/search/generic_search_results.html', {'clients': clients})

    elif model_name == 'proforma':
        proformas = Proforma.objects.filter(
            Q(proforma_number__icontains=query) |
            Q(client__business_name__icontains=query)
        )[:10]
        return render(request, 'commercial/proforma/partials/_proforma_list.html', {'proformas': proformas})

    elif model_name == 'asset':
        assets = Asset.objects.filter(
            Q(name__icontains=query) |
            Q(serial_number__icontains=query)
        )[:10]
        return render(request, 'supply/asset/partials/_asset_list.html', {'assets': assets})

    else:
        return render(request, 'core/search/generic_search_results.html', {})