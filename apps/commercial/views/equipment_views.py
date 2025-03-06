from django.shortcuts import get_object_or_404
from apps.commercial.models.proforma_models import Proforma
from apps.commercial.forms.equipment_forms import EquipmentAddForm


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
        "sales/proforma/equipment/proforma-equipment-list.html",
        {"proforma": proforma}
    )