from decimal import Decimal
from django.shortcuts import get_object_or_404, render
from apps.commercial.models.proforma_models import Proforma, Equipment
from apps.commercial.forms.equipment_forms import EquipmentAddForm, EquipmentFormSet, EquipmentForm


def proforma_equipment_add(request, id):
    proforma = get_object_or_404(Proforma, id=id)
    equipment_form = EquipmentAddForm(request.POST)
    equipment = equipment_form.save(commit=False)
    equipment.proforma = proforma
    equipment.code = equipment.instrument.procedure_code
    equipment.procedure = equipment.instrument.procedure
    equipment.magnitude = equipment.instrument.discipline

    # Determinar el lugar de calibración de forma directa
    if equipment.service_place == "in_situ":
        equipment.calibration_place = proforma.service_address
    elif proforma.service_type == "lo_justo_arequipa":
        equipment.calibration_place = "Av Arequipa"
    elif proforma.service_type == "lo_justo_lima":
        equipment.calibration_place = "Av Lima"
    else:
        equipment.calibration_place = None

    # Calcular el costo total utilizando un diccionario y sum()
    cost_mapping = {
        "calibracion": equipment.quoted_instrument.calibration_cost,
        "verificacion": equipment.quoted_instrument.verification_cost,
        "preventivo": equipment.quoted_instrument.preventive_maintenance_cost or 0,
    }

    selected_services = equipment_form.cleaned_data["service"]
    total_cost = sum(cost_mapping.get(service.type, 0) for service in selected_services)

    # Sumar el costo indirecto, evitando conversiones si ya es Decimal
    if isinstance(equipment.indirect_cost, Decimal):
        total_cost += equipment.indirect_cost
    else:
        total_cost += Decimal(str(equipment.indirect_cost))

    equipment.total = total_cost

    # Guardar el equipo y las relaciones Many-to-Many
    equipment.save()
    equipment_form.save_m2m()

    # Actualizar datos relacionados con la proforma
    proforma.update_labor_data()
    for cost in proforma.additional_costs.all():
        cost.compute_amount()
        cost.save()

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
    return render(request, "commercial/proforma/equipment/_proforma_equipment_form.html",
                  {"formset": formset, "proforma": proforma})


def proforma_equipment_edit(request, id):
    """ Editar un equipo específico en la proforma """
    equipment = get_object_or_404(Equipment, id=id)
    proforma = equipment.proforma

    if request.method == "POST":
        if "cancel" in request.POST:
            return render(request, "commercial/proforma/equipment/_proforma_equipment_list.html",
                          {"proforma": proforma})

        form = EquipmentForm(request.POST, instance=equipment)

        if form.is_valid():
            try:
                equipment = form.save(commit=False)

                # Depuración: Verificar qué se está limpiando
                print(f"Servicios antes de limpiar: {equipment.service.all()}")

                equipment.service.clear()  # ¿Es obligatorio?

                form.save_m2m()  # Guardar relaciones ManyToMany

                # Calcular total y guardar
                equipment.total = equipment.calculate_total()
                equipment.save()

                print(f"Equipo guardado con éxito: {equipment}")

                return render(
                    request,
                    "commercial/proforma/equipment/_proforma_equipment_list.html",
                    {"proforma": proforma}
                )

            except Exception as e:
                print(f"Error al guardar el equipo: {e}")

        else:
            # Depurar errores del formulario
            print("Errores del formulario:", form.errors)

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
        return render(request, 'sales/proforma/equipment/proforma-equipment-list.html', {'proforma': proforma})
