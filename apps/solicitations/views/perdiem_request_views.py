from django.shortcuts import get_object_or_404, redirect, render
from apps.solicitations.forms.perdiem_forms import PerDiemRequestForm
from apps.solicitations.models.perdiem_models import PerDiemRequest
from django.contrib.contenttypes.models import ContentType
from general.forms import CommentForm
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from expenses.forms.perdiem_forms import PerDiemRequestItemForm, PerDiemRequestApprovalForm, PerDiemRequestAdvanceForm
from expenses.models.per_diem_models import PerDiemRequest, PerDiemRequestAdvance, PerDiemSettlement, \
    PerDiemRequestItem, PerDiem, SignatureLog
from django.db.models import Sum
from django.contrib.auth.models import User
from datetime import datetime
from general.models import Laboratory, StartRoute, EndRoute, Area, Vehicle, RoutePair, Comment
from django.contrib import messages
from django.db.models import Sum, F, Case, When, Value, DecimalField
from django.db.models import Case, When, Value, CharField


def perdiem_request_detail(request, pk):
    perdiem_request = get_object_or_404(PerDiemRequest, solicitation__pk=pk)
    form = PerDiemRequestForm(request.POST or None, instance=perdiem_request)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("perdiem_request_detail", pk=pk)
    return render(request, "solicitations/perdiems/perdiem_request_detail.html",
                  {"form": form, "perdiem_request": perdiem_request})


def perdiem_request_plus(request, id):
    perdiem = get_object_or_404(PerDiemRequest, id=id)
    areas = Area.objects.all()
    laboratories = Laboratory.objects.all()
    all_start_routes = StartRoute.objects.all()
    all_end_routes = EndRoute.objects.all()
    persons = User.objects.all()
    all_persons = User.objects.all()
    all_vehicles = Vehicle.objects.all()
    form = CommentForm(request.POST or None, request.FILES or None)
    content_type = ContentType.objects.get_for_model(PerDiemRequest)
    comentarios = Comment.objects.filter(content_type=content_type, object_id=perdiem.id).order_by("-created_at")

    return render(request, 'expenses/perdiemsplus/perdiem_request_plus.html', {
        'perdiem': perdiem,
        'areas': areas,
        'laboratories': laboratories,
        'all_start_routes': all_start_routes,
        'all_end_routes': all_end_routes,
        'persons': persons,
        'all_vehicles': all_vehicles,
        'all_persons': all_persons,
        'model_name': perdiem._meta.model_name,
        'comment_form': form,
        'comentarios': comentarios,
    })


def update_perdiem_request(request, id):
    if request.method == 'POST':
        perdiem = get_object_or_404(PerDiemRequest, id=id)
        area_id = request.POST.get('area')
        laboratory_id = request.POST.get('laboratory')
        from_interested_id = request.POST.get('from_interested')
        oti = request.POST.get('oti')
        requested_date = request.POST.get('requested_date')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        client = request.POST.get('client')
        motive = request.POST.get('motive')
        details = request.POST.get('details')

        if area_id:
            perdiem.area = get_object_or_404(Area, id=area_id)
        if laboratory_id:
            perdiem.laboratory = get_object_or_404(Laboratory, id=laboratory_id)
        if from_interested_id:
            perdiem.from_interested = get_object_or_404(User, id=from_interested_id)

        perdiem.oti = oti
        perdiem.client = client
        perdiem.motive = motive
        perdiem.details = details

        if requested_date:
            perdiem.requested_date = datetime.strptime(requested_date, '%Y-%m-%d').date()
        if start_date:
            perdiem.start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date:
            perdiem.end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        perdiem.save()
        return redirect('perdiem_request_plus', id=id)


def create_per_diem_request(request):
    user = request.user
    perdiem_request = PerDiemRequest.objects.create(
        days=0,
        oti=" ",
        from_interested=user,
        motive=" ",
        details=" ",
        total_expense=0,
        total_expense_dollars=0,
    )

    try:
        alimentacion = PerDiem.objects.get(pk=1)  # ID de alimentación
        alojamiento = PerDiem.objects.get(pk=2)  # ID de alojamiento
        movilidad = PerDiem.objects.get(pk=4)  # ID d emovilidad local
        peaje = PerDiem.objects.get(pk=5)  # ID de peaje
        gasolina = PerDiem.objects.get(pk=6)

        # Crear ítems relacionados
        PerDiemRequestItem.objects.create(
            request_service=perdiem_request,
            item=alimentacion,
            price=alimentacion.price,
            description="Gasto de alimentación",
        )
        PerDiemRequestItem.objects.create(
            request_service=perdiem_request,
            item=alojamiento,
            price=alojamiento.price,
            description="Gasto de alojamiento",
        )
        PerDiemRequestItem.objects.create(
            request_service=perdiem_request,
            item=movilidad,
            price=movilidad.price,
            description="Gasto de movilidad local",
        )

    except PerDiem.DoesNotExist:
        pass

    return redirect('perdiem_request_plus', id=perdiem_request.id)


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
