from apps.solicitations.models.exit_ticket_models import ExitTicket
from apps.solicitations.models.expenses_models import Expenses
from apps.solicitations.models.perdiem_models import PerDiemRequest
from apps.solicitations.models.petty_cash_models import PettyCash
from apps.solicitations.models.mobility_models import MobilitySheet
from apps.solicitations.forms.solicitation_forms import SolicitationForm, SolicitationTypeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from core.models import Period
from apps.solicitations.models.solicitation_models import Solicitation


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
    form_type = SolicitationTypeForm(instance=solicitation)
    form = SolicitationForm(instance=solicitation)

    solicitation_urls_dict = {
        'perdiem_request': 'perdiem_request_detail',
        'exit_ticket': 'exit_ticket_detail',
        'expenses': 'expenses_detail',
        'petty_cash': 'petty_cash_detail',
        'mobility_sheet': 'mobility_sheet_detail'
    }

    solicitation_detail_url = solicitation_urls_dict.get(solicitation.solicitation_type, None)

    context = {
        'solicitation': solicitation,
        'type_form': form_type,
        'form': form,
        'solicitation_detail_url': solicitation_detail_url
    }

    return render(request, 'solicitations/solicitation_detail.html', context)


def solicitation_type_form(request, pk):
    solicitation = get_object_or_404(Solicitation, pk=pk)
    previous_type = solicitation.solicitation_type
    if request.method == 'POST':
        form = SolicitationTypeForm(request.POST, instance=solicitation)
        if form.is_valid():
            solicitation = form.save()
            if solicitation.solicitation_type != previous_type:
                related_models = {
                    'exit_ticket': ExitTicket,
                    'expenses': Expenses,
                    'petty_cash': PettyCash,
                    'mobility_sheet': MobilitySheet,
                    'perdiem_request': PerDiemRequest
                }
                if previous_type in related_models:
                    old_model_class = related_models[previous_type]
                    old_model_class.objects.filter(solicitation=solicitation).delete()
                model_class = related_models.get(solicitation.solicitation_type)
                if model_class:
                    model_class.objects.get_or_create(solicitation=solicitation)
            return redirect('solicitation_detail', pk=solicitation.pk)
    return redirect('solicitation_detail', pk=solicitation.pk)


def solicitation_edit(request, pk):
    solicitation = get_object_or_404(Solicitation, pk=pk)
    form = SolicitationForm(request.POST, instance=solicitation)
    if form.is_valid():
        solicitation = form.save()
        return redirect('solicitation_detail', pk=solicitation.pk)


def solicitation_delete(request, pk):
    solicitation = get_object_or_404(Solicitation, pk=pk)
    if request.user != solicitation.employee and not request.user.is_superuser:
        messages.error(request, "No tienes permiso para eliminar esta solicitud.")
        return redirect('solicitations_list')
    solicitation.delete()
    return redirect('solicitations_list')
