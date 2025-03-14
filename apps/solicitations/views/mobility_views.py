from django.shortcuts import render, redirect, get_object_or_404
from apps.solicitations.forms.mobility_forms import MobilitySheetForm, MobilityItemForm
from apps.solicitations.models.mobility_models import MobilitySheet, MobilityItem


def mobility_sheet_detail(request, pk):
    mobility_sheet = get_object_or_404(MobilitySheet, solicitation__pk=pk)
    detail_form = MobilitySheetForm(request.POST or None, instance=mobility_sheet)
    item_form = MobilityItemForm
    if request.method == "POST" and detail_form.is_valid():
        detail_form.save()
        return redirect(request.path)
    return render(request, "solicitations/mobilities/mobility_sheet_detail.html", {
        "detail_form": detail_form,
        "mobility_sheet": mobility_sheet,
        "item_form": item_form,
    })


def mobility_item_create(request, id):
    if request.method == 'POST':
        mobility_sheet = get_object_or_404(MobilitySheet, id=id)
        form = MobilityItemForm(request.POST)
        if form.is_valid():
            mobility_item = form.save(commit=False)
            mobility_item.mobility_sheet = mobility_sheet
            mobility_item.save()
            return render(request, 'solicitations/mobilities/_mobility_item.html', {
                'mobility_sheet': mobility_sheet,
            })
        else:
            return render(request, 'core/error/_error_message.html', {
                'error': 'Superarias tu limite diario,  oki?  :P'
            }, status=400)


def mobility_item_delete(request, id):
    mobility_item = get_object_or_404(MobilityItem, id=id)
    mobility_sheet = mobility_item.mobility_sheet
    mobility_item.delete()
    return render(request, 'solicitations/mobilities/_mobility_item.html', {
        'mobility_sheet': mobility_sheet,
    })
