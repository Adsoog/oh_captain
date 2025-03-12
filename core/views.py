from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404
from apps.commercial.models.proforma_models import Proforma, Client
from apps.supply.models.asset_models import Asset
from .forms import CommentForm


def generic_search(request):
    model_name = request.GET.get('model')
    query = request.GET.get('q', '').strip()

    if model_name == 'client':
        clients = Client.objects.filter(business_name__icontains=query)[:10]
        return render(request, 'core/search/generic_search_results.html', {'clients': clients})

    elif model_name == 'proforma':
        proformas = Proforma.objects.filter(
            Q(proforma_number__icontains=query) |
            Q(client__business_name__icontains=query)
        )[:10]
        return render(request, 'commercial/proforma/partials/_proforma_list.html', {'proformas': proformas})

    elif model_name == 'asset':
        assets = Asset.objects.filter(
            Q(name__icontains=query) |
            Q(serial_number__icontains=query)
        )[:10]
        return render(request, 'supply/asset/partials/_asset_list.html', {'assets': assets})

    else:
        return render(request, 'core/search/generic_search_results.html', {})


# comments
def comments(request, model_name, object_id):
    content_type = get_object_or_404(ContentType, model=model_name)
    objeto = get_object_or_404(content_type.model_class(), id=object_id)
    comentarios = objeto.comments.all().order_by("-created_at")
    form = CommentForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        comentario = form.save(commit=False)
        comentario.user = request.user
        comentario.content_object = objeto
        comentario.save()
        return render(request, "core/comments/_comments.html", {
            "objeto": objeto,
            "comentarios": objeto.get_comments(),
            "model_name": model_name,
            "comment_form": CommentForm()
        })
    return render(request, "core/comments/_comments.html", {
        "objeto": objeto,
        "comentarios": comentarios,
        "model_name": model_name,
        "comment_form": form
    })
