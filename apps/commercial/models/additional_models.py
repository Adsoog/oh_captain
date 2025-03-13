from decimal import Decimal
from django.db import models
from apps.commercial.models.proforma_models import Proforma


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

class Additional(models.Model):
    proforma = models.ForeignKey(Proforma, on_delete=models.CASCADE, related_name="additional")
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

