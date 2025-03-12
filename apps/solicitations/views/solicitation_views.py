from apps.solicitations.forms.solicitation_forms import SolicitationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from core.models import Period
from apps.solicitations.models.solicitation_models import Solicitation
from apps.solicitations.forms.solicitation_forms import (
    SolicitationForm,
    ExitTicketForm,
    ExpensesForm,
    PettyCashForm,
    MobilitySheetForm,
    PerdiemRequestForm,
)


def auto_solicitation_create(request):
    user = request.user
    today = now().date()
    period = Period.objects.filter(start_date__lte=today, end_date__gte=today).first()
    new_solicitation = Solicitation.objects.create(
        requested_at=today,
        period=period,
        employee=user,
        area=user.employee.area,
        department=user.employee.department,
    )
    return redirect('solicitation_detail', pk=new_solicitation.pk)


def solicitations_list(request):
    solicitations = Solicitation.objects.all()
    context = {
        'solicitations': solicitations,
    }
    return render(request, 'solicitations/solicitations_list.html', context)


def solicitation_detail(request, pk):
    solicitation = get_object_or_404(Solicitation, pk=pk)
    form = SolicitationForm(instance=solicitation)
    detail_form = None
    if solicitation.solicitation_type == 'exit_ticket':
        detail_form = ExitTicketForm(instance=getattr(solicitation, 'exit_ticket_detail', None))
    elif solicitation.solicitation_type == 'expenses':
        detail_form = ExpensesForm(instance=getattr(solicitation, 'expenses_detail', None))
    elif solicitation.solicitation_type == 'petty_cash':
        detail_form = PettyCashForm(instance=getattr(solicitation, 'petty_cash_detail', None))
    elif solicitation.solicitation_type == 'mobility_sheet':
        detail_form = MobilitySheetForm(instance=getattr(solicitation, 'mobility_sheet_detail', None))
    elif solicitation.solicitation_type == 'perdiem_request':
        detail_form = PerdiemRequestForm(instance=getattr(solicitation, 'perdiem_request_detail', None))

    context = {
        'solicitation': solicitation,
        'form': form,
        'detail_form': detail_form,
    }
    return render(request, 'solicitations/solicitation_detail.html', context)


def solicitation_edit(request, pk):
    solicitation = get_object_or_404(Solicitation, pk=pk)
    form = SolicitationForm(request.POST, instance=solicitation)
    if form.is_valid():
        form.save()
        return redirect('solicitation_detail', pk=solicitation.pk)


def solicitation_delete(request):
    pass
