from django.shortcuts import render, get_object_or_404, redirect
from apps.solicitations.forms.expense_forms import ExpensesForm
from apps.solicitations.models.expenses_models import Expenses


def expenses_detail(request, pk):
    expenses = get_object_or_404(Expenses, solicitation__pk=pk)
    detail_form = ExpensesForm(request.POST or None, instance=expenses)

    if request.method == "POST" and detail_form.is_valid():
        detail_form.save()
        return redirect(request.path)

    return render(request, "solicitations/expenses/expenses_detail.html", {
        "detail_form": detail_form,
        "expenses": expenses
    })
