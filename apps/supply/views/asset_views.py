import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from apps.supply.forms.asset_forms import AssetForm
from apps.supply.models.asset_models import Asset, AssetAttributes


def assets_list(request):
    assets = Asset.objects.all()
    return render(request, 'supply/asset/assets_list.html', {'assets': assets})


def asset_detail(request, id):
    asset = get_object_or_404(Asset, id=id)
    requests = asset.requests.all().order_by('-request_date')
    return render(request, 'supply/asset/asset_detail.html', {
        'asset': asset,
        "requests": requests,
    })


def asset_create_edit(request, id=None):
    """
    Vista para crear o editar un activo.
    - Si 'id' es None, se crea un nuevo activo.
    - Si 'id' tiene un valor, se edita el activo existente.
    """
    asset = get_object_or_404(Asset, id=id) if id else None
    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            asset = form.save()
            if not hasattr(asset, 'attributes'):
                AssetAttributes.objects.create(
                    asset=asset,
                    custom_fields={
                        "Color": "Desconocido",
                        "Tamaño": "N/A",
                        "Peso": "N/A",
                    }
                )
            return render(request, 'supply/asset/asset_detail.html', {'asset': asset})
    else:
        form = AssetForm(instance=asset)
    return render(request, 'supply/asset/partials/_asset_form.html', {'form': form, 'asset': asset})


def asset_delete(request, id):
    asset = get_object_or_404(Asset, id=id)
    if request.method == 'POST':
        asset.delete()
        return redirect('assets_list')


def asset_attribute(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    asset_attributes = get_object_or_404(AssetAttributes, asset_id=asset_id)

    if request.method == "POST":
        key = request.POST.get("key")
        value = request.POST.get("value")

        if key:
            asset_attributes.custom_fields[key] = value
            asset_attributes.save(update_fields=["custom_fields"])
            return HttpResponse(status=204)

        new_key = request.POST.get("new_key")
        new_value = request.POST.get("new_value", "")

        if new_key:
            if new_key in asset_attributes.custom_fields:
                return JsonResponse({"error": "El atributo ya existe"}, status=400)

            asset_attributes.custom_fields[new_key] = new_value
            asset_attributes.save(update_fields=["custom_fields"])
            return render(request, "supply/asset/partials/_attribute_row.html", {
                "key": new_key,
                "value": new_value,
                "asset": asset
            })

        return JsonResponse({"error": "No se proporcionaron datos válidos"}, status=400)

    elif request.method == "DELETE":
        key = request.GET.get("key")

        if key and key in asset_attributes.custom_fields:
            del asset_attributes.custom_fields[key]
            asset_attributes.save(update_fields=["custom_fields"])
            return HttpResponse(f"<div class='bg-red-100 text-red-700 p-2 rounded mt-2'>Atributo eliminado</div>")

        return JsonResponse({"error": "Clave no encontrada"}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)
