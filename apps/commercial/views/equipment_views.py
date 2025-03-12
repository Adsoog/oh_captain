from decimal import Decimal
from django.shortcuts import get_object_or_404, render
from apps.commercial.models.proforma_models import Proforma, Equipment
from apps.commercial.forms.equipment_forms import EquipmentAddForm, EquipmentFormSet, EquipmentForm


def proforma_equipment_add(request, id):
    proforma = get_object_or_404(Proforma, id=id)
    equipment_form = EquipmentAddForm(request.POST)
    if equipment_form.is_valid():
        equipment = equipment_form.save(commit=False)
        equipment.proforma = proforma
        equipment.code = equipment.quoted_instrument.procedure_code
        equipment.procedure = equipment.quoted_instrument.procedure
        equipment.magnitude = equipment.quoted_instrument.discipline
        equipment.indirect_cost = Decimal(str(equipment.indirect_cost))

        if equipment.service_place == "in_situ":
            equipment.calibration_place = proforma.service_address
        elif proforma.service_type == "lo_justo_arequipa":
            equipment.calibration_place = "Av Arequipa"
        elif proforma.service_type == "lo_justo_lima":
            equipment.calibration_place = "Av Lima"
        else:
            equipment.calibration_place = None

        selected_services = equipment_form.cleaned_data["service"]
        equipment.total = equipment.calculate_total(selected_services)
        equipment.save()
        equipment_form.save_m2m()

        return render(
            request,
            "commercial/proforma/equipment/_proforma_equipment_list.html",
            {"proforma": proforma}
        )


def proforma_equipment_edit_all(request, id):
    proforma = get_object_or_404(Proforma, id=id)
    equipments = Equipment.objects.filter(proforma=proforma)
    if request.method == 'POST':
        formset = EquipmentFormSet(request.POST, queryset=equipments)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for form, instance in zip(formset.forms, instances):
                instance.skip_update = True
                instance.save()
                instance.service.clear()
                if form.cleaned_data.get("service"):
                    form.save_m2m()
                instance.total = instance.calculate_total()
                instance.save()
            proforma.subtotal, _, proforma.total = proforma.calculate_total()
            proforma.save()
            return render(request, "commercial/proforma/equipment/_proforma_equipment_list.html",
                          {"proforma": proforma})
    else:
        formset = EquipmentFormSet(queryset=equipments)
    return render(request, "commercial/proforma/equipment/_proforma_equipment_edit_all.html",
                  {"formset": formset, "proforma": proforma})


def proforma_equipment_edit(request, id):
    equipment = get_object_or_404(Equipment, id=id)
    proforma = equipment.proforma
    if request.method == "POST":
        if "cancel" in request.POST:
            return render(request, "commercial/proforma/equipment/_proforma_equipment_list.html",
                          {"proforma": proforma})
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            select_services = form.cleaned_data['service']
            equipment.total = equipment.calculate_total(select_services)
            equipment = form.save(commit=False)
            equipment.save()
            form.save_m2m()
            return render(request, "commercial/proforma/equipment/_proforma_equipment_list.html",
                          {"proforma": proforma})
    else:
        form = EquipmentForm(instance=equipment)

    return render(
        request,
        "commercial/proforma/equipment/_proforma_equipment_edit.html",
        {"form": form, "equipment": equipment}
    )


def proforma_equipment_delete(request, id):
    equipment = get_object_or_404(Equipment, id=id)
    if request.method == 'POST':
        proforma = equipment.proforma
        equipment.delete()
        equipment.proforma.update_labor_data()
    for cost in proforma.additional_costs.all():
        cost.compute_amount()
        cost.save()
    return render(request, 'commercial/proforma/equipment/_proforma_equipment_list.html', {'proforma': proforma})
