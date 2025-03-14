from django.shortcuts import render, get_object_or_404, redirect
from apps.solicitations.forms.exit_ticket_forms import ExitTicketForm
from apps.solicitations.models.exit_ticket_models import ExitTicket


def exit_ticket_detail(request, pk):
    exit_ticket = get_object_or_404(ExitTicket, solicitation__pk=pk)
    detail_form = ExitTicketForm(request.POST or None, instance=exit_ticket)
    if request.method == "POST" and detail_form.is_valid():
        detail_form.save()
        return redirect(request.path)
    return render(request, "solicitations/exit_tickets/exit_ticket_detail.html", {
        "detail_form": detail_form,
        "exit_ticket": exit_ticket
    })
