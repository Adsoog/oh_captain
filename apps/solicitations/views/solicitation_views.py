from apps.solicitations.forms.solicitation_forms import SolicitationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from core.models import Period
from apps.solicitations.models.solicitation_models import Solicitation


def solicitations_list(request):
    solicitations = Solicitation.objects.all()
    context = {
        'solicitations': solicitations,
    }
    return render(request, 'solicitations/solicitations_list.html', context)

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

def solicitation_detail(request, pk):
    solicitation= get_object_or_404(Solicitation, pk=pk)
    form = SolicitationForm(instance=solicitation)
    context = {
        'solicitation': solicitation,
        'form': form,
    }
    return render(request, 'solicitations/solicitation_detail.html', context)