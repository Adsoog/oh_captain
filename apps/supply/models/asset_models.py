from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models
from django.utils import timezone


class Asset(models.Model):
    """
    Modelo principal para gestionar todos los activos de la empresa.
    Puede incluir equipos, herramientas, vehículos, software, infraestructura y personal.
    """

    class AssetType(models.TextChoices):
        TOOL = 'tool', _('Herramienta')
        VEHICLE = 'vehicle', _('Vehículo')
        EQUIPMENT = 'equipment', _('Equipo de calibración')
        FACILITY = 'facility', _('Infraestructura')
        SOFTWARE = 'software', _('Software')
        SUPPLY = 'supply', _('Insumo/Repuesto')
        PERSONNEL = 'personnel', _('Personal')
        OTHER = 'other', _('Otro')

    class Status(models.TextChoices):
        AVAILABLE = 'available', _('Disponible')
        IN_USE = 'in_use', _('En uso')
        MAINTENANCE = 'maintenance', _('En mantenimiento')
        DAMAGED = 'damaged', _('Dañado')
        RETIRED = 'retired', _('Retirado')

    name = models.CharField(max_length=150, unique=True)
    asset_type = models.CharField(max_length=50, choices=AssetType.choices, default=AssetType.OTHER)
    serial_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    acquisition_date = models.DateField(blank=True, null=True)
    quantity_available = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.get_asset_type_display()}) - {self.get_status_display()}"


class AssetAttributes(models.Model):
    """
    Almacena información adicional específica de cada activo.
    Se usa JSONField para mayor flexibilidad.
    """
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name="attributes")
    custom_fields = models.JSONField(default=dict)

    def __str__(self):
        return f"Atributos de {self.asset.name}"


class AssetMaintenance(models.Model):
    """
    Registro de mantenimientos, calibraciones o reparaciones de activos.
    """
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="maintenances")
    maintenance_date = models.DateField(auto_now_add=True)
    description = models.TextField()
    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                     null=True)  # Técnico responsable
    next_maintenance_date = models.DateField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.asset.name} - Mantenimiento {self.maintenance_date}"


class AssetMovement(models.Model):
    """
    Registro de movimientos de activos entre ubicaciones o responsables.
    """
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="movements")
    previous_location = models.CharField(max_length=100, blank=True, null=True)
    new_location = models.CharField(max_length=100)
    movement_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                             null=True)  # Responsable del movimiento
    reason = models.TextField(blank=True, null=True)  # Motivo del movimiento

    def __str__(self):
        return f"{self.asset.name} movido de {self.previous_location or 'Desconocido'} a {self.new_location}"

    def save(self, *args, **kwargs):
        """Actualiza la ubicación en Asset cuando se registra un movimiento."""
        self.asset.location = self.new_location
        self.asset.save()
        super().save(*args, **kwargs)


class AssetRequest(models.Model):
    """
    Control de requisiciones de activos. Un usuario solicita un activo y el almacén lo aprueba.
    """

    class RequestStatus(models.TextChoices):
        PENDING = 'pending', _('Pendiente')
        APPROVED = 'approved', _('Aprobado')
        REJECTED = 'rejected', _('Rechazado')
        RETURNED = 'returned', _('Devuelto')

    asset = models.ForeignKey("Asset", on_delete=models.CASCADE, related_name="requests")
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="requests_made")
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="requests_approved")
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=RequestStatus.choices, default=RequestStatus.PENDING)
    request_date = models.DateTimeField(auto_now_add=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    def approve(self, user):
        """
    Aprueba la requisición y asigna el activo al usuario, descontando la cantidad solicitada.
        """
        print(f"🔹 Ejecutando approve() para {self.asset.name} (ID: {self.id})")
        print(f"🔹 Estado actual del activo antes de aprobar: {self.asset.status}")
        print(f"🔹 Cantidad disponible antes de aprobar: {self.asset.quantity_available}")
        print(f"🔹 Cantidad solicitada: {self.quantity}")

        if self.asset.asset_type != Asset.AssetType.PERSONNEL and self.asset.status == Asset.Status.AVAILABLE:
            # 🔹 Verificar si hay suficiente stock
            if self.asset.quantity_available < self.quantity:
                print(f"❌ ERROR: No hay suficiente stock para aprobar la solicitud.")
                return

            print(f"✅ Activo {self.asset.name} está disponible y hay suficiente stock, aprobando...")

            self.status = self.RequestStatus.APPROVED
            self.approved_by = user
            self.approval_date = timezone.now()

            # 🔹 Actualizar cantidad disponible
            self.asset.quantity_available -= self.quantity
            self.asset.save()
            print(f"✅ Nueva cantidad disponible: {self.asset.quantity_available}")

            # 🔹 Registrar movimiento del activo
            movement = AssetMovement.objects.create(
                asset=self.asset,
                previous_location=self.asset.location,
                new_location=f"Asignado a {self.requested_by.username}",
                movement_date=timezone.now(),
                user=self.approved_by,
                reason=f"Entrega de {self.quantity} unidades por requisición aprobada."
            )
            print(f"✅ Movimiento registrado: {movement}")

            self.save(update_fields=["status", "approved_by", "approval_date"])
            print(f"✅ Pedido {self.id} aprobado y guardado en la base de datos.")

        else:
            print(
                f"❌ ERROR: El activo {self.asset.name} NO ESTÁ DISPONIBLE para aprobación. Estado actual: {self.asset.status}")

    def reject(self):
        """
        Rechaza la requisición.
        """
        self.status = self.RequestStatus.REJECTED
        self.save()

    def return_asset(self):
        """
    Marca el activo como devuelto y devuelve la cantidad al stock.
        """
        if self.status == self.RequestStatus.APPROVED:
            self.status = self.RequestStatus.RETURNED
            self.return_date = timezone.now()

            # 🔹 Devolver la cantidad al stock
            self.asset.quantity_available += self.quantity
            self.asset.save()
            print(f"✅ Activo {self.asset.name} devuelto. Nueva cantidad disponible: {self.asset.quantity_available}")

            # 🔹 Registrar el movimiento de devolución
            AssetMovement.objects.create(
                asset=self.asset,
                previous_location=f"Asignado a {self.requested_by.username}",
                new_location="Almacén / Disponible",
                movement_date=timezone.now(),
                user=self.requested_by,
                reason=f"Devolución de {self.quantity} unidades."
            )

            self.save()

    def __str__(self):
        return f"Requisición de {self.asset.name} por {self.requested_by.username} ({self.get_status_display()})"
