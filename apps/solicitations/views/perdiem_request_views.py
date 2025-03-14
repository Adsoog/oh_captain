from django.shortcuts import get_object_or_404, redirect, render
from apps.solicitations.forms.perdiem_forms import PerDiemRequestForm
from apps.solicitations.models.perdiem_models import PerDiemRequest


def perdiem_request_detail(request, pk):
    perdiem_request = get_object_or_404(PerDiemRequest, solicitation__pk=pk)
    form = PerDiemRequestForm(request.POST or None, instance=perdiem_request)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("perdiem_request_detail", pk=pk)
    return render(request, "solicitations/perdiems/perdiem_request_detail.html",
                  {"form": form, "perdiem_request": perdiem_request})
