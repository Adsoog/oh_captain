import math
from decimal import Decimal
from django.conf import settings
from django.db import models
from apps.commercial.models.client_models import Branch, Contact, Client
from apps.commercial.models.instrument_models import Instrument

class Proforma(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Borrador'),
        ('completed', 'Completada'),
        ('sent', 'Enviada'),
        ('rejected', 'Rechazada'),
        ('approved', 'Aprobada'),
        ('accepted', 'Aceptada'),
    ]

    SERVICE_CHOICES = [
        ('lo_justo_arequipa', 'LO JUSTO AREQUIPA'),
        ('lo_justo_lima', 'LO JUSTO LIMA'),
        ('in_situ', 'IN SITU'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="proformas", null=True, blank=True)
    contacts = models.ManyToManyField(Contact, blank=True, null=True)
    request_date = models.DateField(blank=True, null=True)
    proforma_date = models.DateField(blank=True, null=True)
    payment_method = models.CharField(max_length=50, default="Contado", choices=[('contado', 'Al contado'), ('credito', 'Credito')])
    service_type = models.CharField(max_length=50, default="lo_justo", choices=SERVICE_CHOICES )
    offer_validity = models.IntegerField(default=15)
    service_address = models.CharField(max_length=255)
    certificate_owner = models.CharField(max_length=255, blank=True, null=True)
    certificate_address = models.CharField(max_length=255, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    igv = models.DecimalField(max_digits=5, decimal_places=2, default=18.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="children")
    correlative = models.CharField(max_length=20, unique=True, blank=True, null=True)
    version = models.CharField(max_length=50, blank=True, null=True)
    sales_advisor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    total_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_days = models.IntegerField(default=0)
    total_workers = models.IntegerField(default=0)
    total_km = models.IntegerField(default=0.00)

    def update_labor_data(self):
        equipment_list = self.equipments.filter(service_place='in_situ')
        total_hours = sum(eq.instrument.man_hours for eq in equipment_list if eq.instrument is not None)
        max_workers = max((eq.instrument.necessary_workers for eq in equipment_list if eq.instrument),default=0)
        self.total_hours = total_hours
        self.total_days = math.ceil(total_hours / 8)
        self.total_workers = max_workers
        self.save()

    def calculate_total(self):
        if not self.pk:
            return Decimal('0.00'), Decimal('0.00'), Decimal('0.00')
        subtotal = sum([equipment.total for equipment in self.equipments.all()])
        additional_costs = sum(cost.amount for cost in self.additional_costs.filter(enabled=True))
        subtotal += additional_costs
        igv_percentage = Decimal(str(self.igv)) / Decimal('100')
        igv_amount = subtotal * igv_percentage
        total = subtotal + igv_amount
        return subtotal, igv_amount, total

    def save(self, *args, **kwargs):
        self.subtotal, _, self.total = self.calculate_total()
        super().save(*args, **kwargs)


class Service(models.Model):
    SERVICE_TYPES = [
        ('preventivo', 'PREVENTIVO'),
        ('calibracion', 'CALIBRACIÓN'),
        ('verificacion', 'VERIFICACIÓN')
    ]
    type = models.CharField(max_length=12, choices=SERVICE_TYPES)

    def __str__(self):
        return f"{self.type}"


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
    service_place = models.CharField(max_length=50, default="lo_justo", choices=SERVICE_CHOICES, blank=True, null=True )
    calibration_place = models.TextField(blank=True, null=True)
    service = models.ManyToManyField(Service, blank=True, null=True)
    indirect_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quoted_instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.brand} {self.model} - {self.serial_number if self.serial_number else 'No Serial Number'}"


class AdditionalCostParameter(models.Model):
    COST_TYPES = [
        ('transport_personnel', 'Transporte de personal'),
        ('transport_equipment', 'Transporte de equipos'),
        ('lodging', 'Alojamiento de personal'),
        ('food', 'Alimentación de personal'),
        ('insurance', 'Seguro SCTR'),
        ('curses', 'Cursos para el personal'),
        ('rental', 'Alquiler de equipo o servicio'),
        ('overtime', 'Tiempo suplementario de personal técnico'),
    ]
    cost_type = models.CharField(max_length=50, choices=COST_TYPES, unique=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_cost_type_display()} - Precio base: S/. {self.base_price}"


class AdditionalCost(models.Model):
    proforma = models.ForeignKey(Proforma, on_delete=models.CASCADE, related_name="additional_costs")
    parameter = models.ForeignKey(AdditionalCostParameter, on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.parameter.get_cost_type_display()} - S/. {self.amount}"

    def compute_amount(self):
        base_price = self.parameter.base_price
        total_days = Decimal(self.proforma.total_days)
        total_workers = Decimal(self.proforma.total_workers)
        total_km = Decimal(self.proforma.total_km)
        cost_type = self.parameter.cost_type
        if cost_type == 'lodging':
            self.amount = base_price * total_workers * total_days
        elif cost_type == 'food':
            self.amount = base_price * total_workers * total_days
        elif cost_type == 'transport_personnel':
            self.amount = base_price * total_km
        elif cost_type == 'transport_equipment':
            self.amount = base_price * total_km
        elif cost_type == 'overtime':
            self.amount = base_price
        return self.amount