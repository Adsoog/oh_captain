from django.shortcuts import render, get_object_or_404, redirect
from apps.solicitations.forms.petty_cash_forms import PettyCashForm
from apps.solicitations.models.petty_cash_models import PettyCash


def petty_cash_detail(request, pk):
    petty_cash = get_object_or_404(PettyCash, solicitation__pk=pk)
    detail_form = PettyCashForm(request.POST or None, instance=petty_cash)

    if request.method == "POST" and detail_form.is_valid():
        detail_form.save()
        return redirect(request.path)

    return render(request, "solicitations/pettycash/petty_cash_detail.html", {
        "detail_form": detail_form,
        "petty_cash": petty_cash
    })
