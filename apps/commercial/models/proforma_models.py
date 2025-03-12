import math
from decimal import Decimal
from django.conf import settings
from django.db import models
from apps.commercial.models.client_models import Branch, Contact, Client
from apps.commercial.models.instrument_models import Instrument


class Service(models.Model):
    SERVICE_TYPES = [
        ('preventivo', 'PREVENTIVO'),
        ('calibracion', 'CALIBRACIÓN'),
        ('verificacion', 'VERIFICACIÓN')
    ]
    type = models.CharField(max_length=12, choices=SERVICE_TYPES)

    def __str__(self):
        return f"{self.type}"


class Proforma(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Borrador'),
        ('completed', 'Completada'),
        ('sent', 'Enviada'),
        ('rejected', 'Rechazada'),
        ('approved', 'Aprobada'),
        ('accepted', 'Aceptada'),
    ]
    SERVICE_TYPE_CHOICES = [
        ('lo_justo_arequipa', 'LO JUSTO AREQUIPA'),
        ('lo_justo_lima', 'LO JUSTO LIMA'),
        ('in_situ', 'IN SITU'),
    ]
    correlative = models.CharField(max_length=20, unique=True, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="proformas", null=True, blank=True)
    contacts = models.ManyToManyField(Contact, blank=True, null=True)
    request_date = models.DateField(blank=True, null=True)
    proforma_date = models.DateField(blank=True, null=True)
    service_type = models.CharField(max_length=50, default="lo_justo", choices=SERVICE_TYPE_CHOICES)
    offer_validity = models.IntegerField(default=15)
    service_address = models.CharField(max_length=255)
    certificate_owner = models.CharField(max_length=255, blank=True, null=True)
    certificate_address = models.CharField(max_length=255, blank=True, null=True)
    sales_advisor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')


class ProformaParameters(models.Model):
    proforma = models.OneToOneField(Proforma, on_delete=models.CASCADE, related_name='parameters')
    total_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_days = models.IntegerField(default=0)
    total_workers = models.IntegerField(default=0)
    total_km = models.IntegerField(default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    igv = models.DecimalField(max_digits=5, decimal_places=2, default=18.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


class Equipment(models.Model):
    SERVICE_CHOICES = [
        ('lo_justo', 'LO JUSTO'),
        ('in_situ', 'IN SITU'),
    ]
    proforma = models.ForeignKey(Proforma, on_delete=models.CASCADE, related_name="equipments")
    brand = models.CharField(max_length=255, blank=True, null=True)
    model = models.CharField(max_length=255, blank=True, null=True)
    specifications = models.TextField(blank=True, null=True)
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    code = models.CharField(max_length=50, blank=True, null=True)
    procedure = models.TextField(blank=True, null=True)
    magnitude = models.CharField(max_length=100, blank=True, null=True)
    service_place = models.CharField(max_length=50, default="lo_justo", choices=SERVICE_CHOICES, blank=True, null=True)
    calibration_place = models.TextField(blank=True, null=True)
    service = models.ManyToManyField(Service, blank=True, null=True)
    indirect_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quoted_instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)

    def calculate_total(self, services):
        total = Decimal('0.00')
        SERVICE_COST_MAP = {
            'calibracion': 'calibration_cost',
            'verificacion': 'verification_cost',
            'preventivo': 'preventive_maintenance_cost'
        }
        for service in services:
            cost_field = SERVICE_COST_MAP.get(service.type)
            if cost_field:
                service_cost = getattr(self.quoted_instrument, cost_field, Decimal('0.00'))
                if service_cost is not None:
                    total += service_cost
        total += self.indirect_cost
        return total

    def __str__(self):
        return f"{self.brand} {self.model} - {self.serial_number if self.serial_number else 'No Serial Number'}"
