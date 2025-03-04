from django.shortcuts import render
from apps.requests.models.request_models import Request


def requests_list(request):
    requests = Request.objects.all()
    context = {
        'requests': requests,
    }
    return render(request, 'requests/requests_list.html', context)
