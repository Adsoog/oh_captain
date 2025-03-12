from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from apps.supply.models.asset_models import AssetRequest
from apps.supply.forms.asset_forms import AssetRequestForm


@login_required
def asset_request(request):
    """
    Permite a los usuarios solicitar activos desde un formulario.
    Se mantiene en la misma página después del envío exitoso.
    """
    form = AssetRequestForm()

    if request.method == "POST":
        form = AssetRequestForm(request.POST)
        if form.is_valid():
            asset_request = form.save(commit=False)
            asset_request.requested_by = request.user
            asset_request.status = AssetRequest.RequestStatus.PENDING
            asset_request.request_date = timezone.now()
            asset_request.save()

            messages.success(request, "Tu solicitud ha sido enviada correctamente.")
            form = AssetRequestForm()  # 🔹 Limpiar el formulario después del envío exitoso

    return render(request, "supply/request/asset_request.html", {"form": form})


def approve_request(request, request_id):
    print(f"🔹 Usuario actual: {request.user} ({'Admin' if request.user.is_staff else 'Employee'})")
    print(f"🔹 ¿Es autenticado?: {request.user.is_authenticated}")

    asset_request = get_object_or_404(AssetRequest, id=request_id)

    print(f"🔹 Estado actual del pedido: {asset_request.status}")

    if not request.user.is_authenticated:
        print("❌ Usuario no autenticado. Redirigiendo...")
        messages.error(request, "No tienes permisos para aprobar solicitudes.")
        return redirect("request_list")

    # 🔹 Llamamos al método approve() en el modelo
    print("✅ Llamando al método approve()...")
    asset_request.approve(user=request.user)

    # 🔹 Verificar si el estado realmente cambió
    asset_request.refresh_from_db()  # Recargar el objeto desde la base de datos
    print(f"🔹 Nuevo estado del pedido después de approve(): {asset_request.status}")

    if asset_request.status != AssetRequest.RequestStatus.APPROVED:
        print("❌ ERROR: El estado no cambió correctamente.")

    messages.success(request,
                     f"Solicitud de {asset_request.asset.name} aprobada y asignada a {asset_request.requested_by.username}.")
    return redirect("assets_list")


def reject_request(request, request_id):
    """
Vista para que un administrador rechace una solicitud de activo.
    """
    asset_request = get_object_or_404(AssetRequest, id=request_id)

    if not request.user.is_staff:  # 🔹 Solo admins pueden rechazar
        messages.error(request, "No tienes permisos para rechazar solicitudes.")
        return redirect("request_list")

    # ✅ Llamamos al método `reject()` del modelo
    asset_request.reject()

    messages.warning(request, f"Solicitud de {asset_request.asset.name} rechazada.")
    return redirect("assets_list")
