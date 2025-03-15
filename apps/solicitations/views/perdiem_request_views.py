from apps.solicitations.forms.perdiem_forms import PerDiemRequestForm
from apps.solicitations.models.perdiem_models import PerDiemRequest
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User


def perdiem_request_detail(request, pk):
    perdiem_request = get_object_or_404(PerDiemRequest, solicitation__pk=pk)
    form = PerDiemRequestForm(instance=perdiem_request)
    return render(request, "solicitations/perdiems/perdiem_request_detail.html",
                  {"form": form, "perdiem_request": perdiem_request})


def add_vehicle_to_perdiem(request, id):
    if request.method == 'POST':
        perdiem = get_object_or_404(PerDiemRequest, id=id)
        vehicle_id = request.POST.get('vehicle')
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        perdiem.vehicles.add(vehicle)

        try:
            peaje = PerDiem.objects.get(pk=5)  # ID de peaje
            gasolina = PerDiem.objects.get(pk=6)  # ID de gasolina

            existing_items = PerDiemRequestItem.objects.filter(
                request_service=perdiem,
                item__in=[peaje, gasolina]
            ).values_list('item', flat=True)

            if peaje.pk not in existing_items:
                PerDiemRequestItem.objects.create(
                    request_service=perdiem,
                    item=peaje,
                    price=peaje.price,
                    description="Gasto de peaje",
                )
            if gasolina.pk not in existing_items:
                PerDiemRequestItem.objects.create(
                    request_service=perdiem,
                    item=gasolina,
                    price=gasolina.price,
                    description="Gasto de gasolina",
                )

        except PerDiem.DoesNotExist:
            pass

        return redirect('perdiem_request_plus', id=perdiem.id)


def get_persons_popup(request, id):
    perdiem = get_object_or_404(PerDiemRequest, id=id)
    all_persons = User.objects.all().order_by('last_name', 'first_name')

    return render(request, 'expenses/perdiemsplus/partials/persons_modal.html', {
        'perdiem': perdiem,
        'all_persons': all_persons,
    })


def remove_vehicle_from_perdiem(request, id, vehicle_id):
    if request.method == 'POST':
        perdiem = get_object_or_404(PerDiemRequest, id=id)
        vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
        perdiem.vehicles.remove(vehicle)
        all_vehicles = Vehicle.objects.all()

        return render(request, 'expenses/perdiemsplus/partials/perdiem_vehicles.html', {
            'perdiem': perdiem,
            'all_vehicles': all_vehicles,
        })


def add_route_pair_to_perdiem(request, id):
    if request.method == 'POST':
        perdiem = get_object_or_404(PerDiemRequest, id=id)
        start_route_id = request.POST.get('start_route')
        end_route_id = request.POST.get('end_route')

        # Validar y crear el par de rutas
        if start_route_id and end_route_id:
            start_route = get_object_or_404(StartRoute, id=start_route_id)
            end_route = get_object_or_404(EndRoute, id=end_route_id)
            route_pair, created = RoutePair.objects.get_or_create(start_route=start_route, end_route=end_route)
            perdiem.route_pairs.add(route_pair)

        # Renderizar el template actualizado
        all_start_routes = StartRoute.objects.all()
        all_end_routes = EndRoute.objects.all()
        return render(request, 'expenses/perdiemsplus/partials/perdiem_routes.html', {
            'perdiem': perdiem,
            'all_start_routes': all_start_routes,
            'all_end_routes': all_end_routes,
        })


def remove_route_pair_from_perdiem(request, perdiem_id, pair_id):
    if request.method == 'POST':
        perdiem = get_object_or_404(PerDiemRequest, id=perdiem_id)
        route_pair = get_object_or_404(RoutePair, id=pair_id)

        # Eliminar la relación entre el par de rutas y la solicitud
        perdiem.route_pairs.remove(route_pair)

        # Renderizar el template actualizado
        all_start_routes = StartRoute.objects.all()
        all_end_routes = EndRoute.objects.all()
        return render(request, 'expenses/perdiemsplus/partials/perdiem_routes.html', {
            'perdiem': perdiem,
            'all_start_routes': all_start_routes,
            'all_end_routes': all_end_routes,
        })


def add_persons_to_perdiem(request, id):
    if request.method == 'POST':
        perdiem = get_object_or_404(PerDiemRequest, id=id)
        person_ids = request.POST.getlist('persons')
        persons = User.objects.filter(id__in=person_ids)
        perdiem.persons.add(*persons)
        return redirect('perdiem_request_plus', id=perdiem.id)


def normal_add_persons_to_perdiem(request, id):
    if request.method == 'POST':
        perdiem = get_object_or_404(PerDiemRequest, id=id)
        person_ids = request.POST.getlist('persons')
        persons = User.objects.filter(id__in=person_ids)
        perdiem.persons.add(*persons)

        # Renderizar el parcial actualizado
        return render(request, 'expenses/perdiemsplus/partials/perdiem_persons.html', {
            'perdiem': perdiem,
            'all_persons': User.objects.all(),
        })


def remove_person_from_perdiem(request, id, person_id):
    if request.method == 'POST':
        perdiem = get_object_or_404(PerDiemRequest, id=id)
        person = get_object_or_404(User, id=person_id)
        perdiem.persons.remove(person)

        return redirect('perdiem_request_plus', id=perdiem.id)


def per_diem_item_form(request, id, item_id=None):
    perdiem = get_object_or_404(PerDiemRequest, id=id)
    item = None

    if item_id:
        item = get_object_or_404(PerDiemRequestItem, id=item_id)

    if request.method == 'POST':
        form = PerDiemRequestItemForm(request.POST, instance=item)
        if form.is_valid():
            perdiem_item = form.save(commit=False)
            perdiem_item.request_service = perdiem
            perdiem_item.save()
            return redirect('perdiem_request_plus', id=perdiem.id)
    else:
        form = PerDiemRequestItemForm(instance=item)

    return render(request, 'expenses/perdiemsplus/partials/perdiem_item_form.html', {
        'form': form,
        'perdiem': perdiem,
        'item': item,
    })


def edit_per_diem_item(request, id, item_id):
    perdiem = get_object_or_404(PerDiemRequest, id=id)
    item = get_object_or_404(PerDiemRequestItem, id=item_id)

    if request.method == 'POST':
        form = PerDiemRequestItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('perdiem_request_plus', id=perdiem.id)
    else:
        form = PerDiemRequestItemForm(instance=item)

    return render(request, 'expenses/perdiemsplus/partials/edit_perdiem_item_form.html', {
        'form': form,
        'perdiem': perdiem,
        'item': item,
    })


def delete_per_diem_item(request, id, item_id):
    if request.method == 'POST':
        perdiem = get_object_or_404(PerDiemRequest, id=id)
        item = get_object_or_404(PerDiemRequestItem, id=item_id)

        if item.item.item in ['alimentacion', 'alojamiento']:
            return JsonResponse({'error': 'No puedes eliminar items de Alimentación o Alojamiento.'}, status=403)

        item.delete()

        # Recalcular los totales de PerDiemRequest
        perdiem._calculate_totals()
        perdiem.save(update_fields=['total_expense', 'total_expense_dollars'])

        return redirect('perdiem_request_plus', id=perdiem.id)


def approve_signature(request, perdiem_id, signature_type):
    if request.method == 'POST':
        perdiem = get_object_or_404(PerDiemRequest, id=perdiem_id)

        if signature_type == 'applicant' and not perdiem.applicant_signature:
            perdiem.applicant_signature = True
            SignatureLog.objects.create(
                request_service=perdiem,
                signature_type='applicant',
                user=request.user
            )
        elif signature_type == 'supervisor' and not perdiem.supervisor_signature:
            perdiem.supervisor_signature = True
            SignatureLog.objects.create(
                request_service=perdiem,
                signature_type='supervisor',
                user=request.user
            )
        elif signature_type == 'accounting' and not perdiem.accounting_signature:
            perdiem.accounting_signature = True
            SignatureLog.objects.create(
                request_service=perdiem,
                signature_type='accounting',
                user=request.user
            )
        perdiem.save()
        return render(request, 'expenses/perdiemsplus/partials/approvals_partial.html', {'perdiem': perdiem})

    return JsonResponse({'error': 'Invalid request'}, status=400)


def reject_perdiem(request, perdiem_id):
    if request.method == 'POST':
        perdiem = get_object_or_404(PerDiemRequest, id=perdiem_id)
        perdiem.status = 'rejected'
        perdiem.save()
        print(perdiem.status)
        return render(request, 'expenses/perdiemsplus/partials/approvals_partial.html', {'perdiem': perdiem})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def perdiem_request_plus_approval(request, id):
    perdiem = get_object_or_404(PerDiemRequest, id=id)
    advance_form = PerDiemRequestAdvanceForm()

    if request.method == 'POST':
        advance_form = PerDiemRequestAdvanceForm(request.POST, request.FILES)
        if advance_form.is_valid():
            advance = advance_form.save(commit=False)
            advance.request = perdiem
            advance.save()
            return redirect('perdiem_request_plus', id=perdiem.id)

    return render(request, 'expenses/perdiemsplus/partials/perdiem_advance.html', {
        'advance_form': advance_form,
        'perdiem': perdiem,
    })
