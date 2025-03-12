from django.utils.timezone import now
from django.shortcuts import render, get_object_or_404, redirect
from apps.planning.forms.work_orders_forms import WorkOrderForm, WorkOrderEquipmentForm, WorkOrderAssetForm, \
    WorkOrderWorkerForm
from apps.planning.models.workorder_models import WorkOrder


def work_orders_list(request):
    orders = WorkOrder.objects.all()
    return render(request, 'planning/orders/work_orders_list.html', {'orders': orders})


def work_order_detail(request, id):
    order = get_object_or_404(WorkOrder, id=id)

    # Formularios prellenados con la información actual
    equipment_form = WorkOrderEquipmentForm(instance=order)
    asset_form = WorkOrderAssetForm(instance=order)
    worker_form = WorkOrderWorkerForm(instance=order)

    if request.method == "POST":
        if "update_equipment" in request.POST:
            equipment_form = WorkOrderEquipmentForm(request.POST, instance=order)
            if equipment_form.is_valid():
                equipment_form.save()
                return redirect('work_order_detail', id=order.id)

        if "update_asset" in request.POST:
            asset_form = WorkOrderAssetForm(request.POST, instance=order)
            if asset_form.is_valid():
                asset_form.save()
                return redirect('work_order_detail', id=order.id)

        if "update_worker" in request.POST:
            worker_form = WorkOrderWorkerForm(request.POST, instance=order)
            if worker_form.is_valid():
                worker_form.save()
                return redirect('work_order_detail', id=order.id)

    return render(request, 'planning/orders/work_order_detail.html', {
        'order': order,
        'equipment_form': equipment_form,
        'asset_form': asset_form,
        'worker_form': worker_form,
    })


def work_order_edit(request, id):
    order = get_object_or_404(WorkOrder, id=id)
    if request.method == 'POST':
        form = WorkOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('work_order_detail', id=order.id)
    else:
        form = WorkOrderForm(instance=order)
    return render(request, 'planning/orders/work_orders_list.html', {'form': form, 'order': order})


def work_order_delete(request, id):
    order = get_object_or_404(WorkOrder, id=id)
    if request.method == 'POST':
        order.delete()
        return redirect('work_orders_list')
