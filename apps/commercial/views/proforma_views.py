from django.utils.timezone import now
from django.shortcuts import render, get_object_or_404, redirect
from apps.commercial.forms.equipment_forms import EquipmentAddForm
from apps.commercial.forms.proforma_forms import ProformaForm
from apps.commercial.models.proforma_models import Proforma


def proformas_list(request):
    user = request.user
    proformas = Proforma.objects.all()
    return render(request, 'commercial/proforma/proformas_list.html', {'proformas': proformas})


def auto_proforma_create(request):
    if request.method == 'POST':
        user = request.user
        today = now().date()
        proforma = Proforma.objects.create(
            request_date=today,
            proforma_date=today,
            sales_advisor=user,
        )
        return redirect('proforma_detail', id=proforma.id)
    else:
        return redirect('proformas_list')


def proforma_detail(request, id):
    proforma = get_object_or_404(Proforma, id=id)
    form = ProformaForm(instance=proforma)
    equipment_add_form = EquipmentAddForm()
    return render(request, 'commercial/proforma/proforma_detail.html', {
        'proforma': proforma,
        'form': form,
        'equipment_add_form': equipment_add_form,
    })


def proforma_edit(request, id):
    proforma = get_object_or_404(Proforma, id=id)
    if request.method == 'POST':
        form = ProformaForm(request.POST, instance=proforma)
        if form.is_valid():
            form.save()
            return redirect('proforma_detail', id=proforma.id)
    else:
        form = ProformaForm(instance=proforma)
    return render(request, 'commercial/proforma/partials/_proforma_detail.html', {'form': form, 'proforma': proforma})


def proforma_delete(request, id):
    proforma = get_object_or_404(Proforma, id=id)
    if request.method == 'POST':
        proforma.delete()
        return redirect('proformas_list')
