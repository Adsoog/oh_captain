from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from apps.solicitations.forms.expense_forms import ExpenseItemForm
from apps.solicitations.models.expenses_models import Expense, ExpenseItem
from apps.solicitations.utils import provider_name


def expense_detail(request, pk):
    expense = get_object_or_404(Expense, solicitation__pk=pk)
    item_form = ExpenseItemForm()
    return render(request, "solicitations/expenses/expense_detail.html", {
        "item_form": item_form,
        "expense": expense
    })


def expense_item_create(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        item_form = ExpenseItemForm(request.POST, request.FILES)
        if item_form.is_valid():
            expense_item = item_form.save(commit=False)
            expense_item.provider_name = provider_name(expense_item.ruc_or_dni)
            expense_item.expense = expense
            expense_item.save()
            return render(request, 'solicitations/expenses/expense_item.html', {
                'expense': expense,
                'item_form': ExpenseItemForm()
            })
    return HttpResponse("Formulario inválido", status=400)


def expense_item_edit(request, pk):
    item = get_object_or_404(ExpenseItem, pk=pk)
    if request.method == 'POST':
        item_form = ExpenseItemForm(request.POST, request.FILES, instance=item)
        if item_form.is_valid():
            item = item_form.save(commit=False)
            item.provider_name = provider_name(item.ruc_or_dni)
            item.save()
            return render(request, 'solicitations/expenses/expense_item.html', {
                'item': item,
            })
    else:
        item_form = ExpenseItem(instance=item)
        return render(request, 'solicitations/expenses/expense_item.html', {
            'item_form': item_form,
            'item': item,
        })


def expense_item_delete(request, pk):
    item = get_object_or_404(ExpenseItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        return render(request, 'solicitations/expenses/expense_item.html', {})
    return HttpResponseBadRequest("Método no permitido", status=405)
