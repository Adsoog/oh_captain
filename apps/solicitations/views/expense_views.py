from apps.solicitations.forms.expense_forms import ExpenseItemForm
from django.shortcuts import get_object_or_404, redirect
from apps.solicitations.models.expenses_models import Expense, ExpenseItem
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render


def expense_detail(request, pk):
    expense = get_object_or_404(Expense, id=id)
    item_form = ExpenseItemForm()
    return render(request, "solicitations/expenses/expense_detail.html", {
        "item_form": item_form,
        "expense": expense
    })


def expense_item_create(request, report_id):
    if request.method == 'POST':
        form = ExpenseItemForm(request.POST, request.FILES)
        if form.is_valid():
            expenditure_detail = form.save(commit=False)
            _, _, razon_social = obtener_estado_condicion(expenditure_detail.ruc_or_dni)
            expenditure_detail.provider_name = razon_social
            expenditure_detail.report = report
            expenditure_detail.save()

            return render(request, 'expenses/expenditures/partials/expenditure_gastos.html', {
                'report': report,
                'item_form': ExpenditureDetailForm(),  # Crear un nuevo formulario vacío
            })
    return HttpResponse("Formulario inválido", status=400)


def expense_item_edit(request, detail_id):
    item = get_object_or_404(ExpenditureDetail, id=detail_id)
    if request.method == 'POST':
        form = ExpenditureDetailForm(request.POST, request.FILES, instance=detail)
        if form.is_valid():
            # Guardamos sin comprometer a la BD para poder modificar provider_name
            detail = form.save(commit=False)
            # Actualizamos provider_name con la razón social obtenida
            _, _, razon_social = obtener_estado_condicion(detail.ruc_or_dni)
            detail.provider_name = razon_social
            detail.save()  # Guardamos la instancia actualizada

            # Renderizamos la fila en modo 'lectura' ya actualizada
            return render(request, 'expenses/expenditures/partials/expenditure_detail_row.html', {
                'detail': detail,
            })
        else:
            # Renderizamos el mismo partial con el formulario (errores)
            return render(request, 'expenses/expenditures/partials/expenditure_detail_edit_form.html', {
                'form': form,
                'detail': detail,
            }, status=400)
    else:
        # GET: devolvemos el formulario
        form = ExpenditureDetailForm(instance=detail)
        return render(request, 'expenses/expenditures/partials/expenditure_detail_edit_form.html', {
            'form': form,
            'detail': detail,
        })


def expense_item_delete(request, id):
    item = get_object_or_404(ExpenseItem, id=id)
    if request.method == 'POST':
        item.delete()
        return render(request, 'expenses/expenditures/partials/expenditure_detail_deleted.html', {})

    return HttpResponseBadRequest("Método no permitido", status=405)
