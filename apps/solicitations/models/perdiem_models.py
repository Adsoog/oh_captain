from django.conf import settings
from django.db import models

from apps.solicitations.models.solicitation_models import Solicitation
from apps.supply.models.asset_models import Asset


class PerDiem(models.Model):
    PER_DIEM_CHOICES = [
        ('alimentacion', 'Alimentación'),
        ('movilidad_local', 'Movilidad local'),
        ('pasaje_terrestre', 'Pasaje terrestre'),
        ('peaje', 'Peaje'),
        ('pasaje_aereo', 'Pasaje aéreo'),
        ('alojamiento', 'Alojamiento'),
        ('combustible', 'Combustible'),
        ('reparaciones', 'Reparaciones'),
        ('otros', 'Otros'),
    ]
    TYPE_CHOICES = [
        ('diario', 'Gasto diario'),
        ('unico', 'Gasto único'),
    ]

    item = models.CharField(max_length=20, choices=PER_DIEM_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amount_per_day = models.PositiveIntegerField(default=1)
    type_item = models.CharField(max_length=10, choices=TYPE_CHOICES, default='unico')
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Viatico"
        verbose_name_plural = "Viaticos"


    def __str__(self):
        return f"{self.get_item_display()}"


class PerDiemRequest(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Borrador'),
        ('created', 'Creada'),
        ('approved_by_supervisor', 'V°B° de Jefatura'),
        ('approved_by_accounting', 'V°B° de Contabilidad'),
        ('paid', 'Abonada'),
        ('rendered', 'Rendida'),
        ('approved_rendering', 'Rendición aprobada'),
        ('closed', 'Cerrada'),
        ('rejected', 'Rechazada'),
    ]
    solicitation = models.OneToOneField(Solicitation, on_delete=models.CASCADE, related_name="perdiem")
    vehicles = models.ManyToManyField(Asset, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    days = models.IntegerField(null=True, blank=True)
    persons = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='viajantes')
    details = models.TextField(null=True, blank=True)
    total_expense = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.details} - Dias: {self.days}"

class PerDiemRequestItem(models.Model):
    CURRENCY_CHOICES = [
        ('DOLARES', 'Dolares'),
        ('SOLES', 'Soles')
    ]
    request_service = models.ForeignKey(PerDiemRequest, related_name='perdiem_request_item', on_delete=models.CASCADE)
    item = models.ForeignKey(PerDiem, related_name='perdiem_item', on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=40, blank=True, null=True)
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default='SOLES')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    state = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Item de solicitude"
        verbose_name_plural = "Items de solicitudes"

    def __str__(self):
        return f"{self.item}"
