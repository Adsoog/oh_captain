from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


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
