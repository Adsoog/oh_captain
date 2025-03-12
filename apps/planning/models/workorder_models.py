from django.conf import settings
from django.db import models
from apps.supply.models.asset_models import Asset
from apps.commercial.models.proforma_models import Proforma, Equipment


class WorkOrder(models.Model):
    proforma = models.ForeignKey(Proforma, on_delete=models.CASCADE, related_name='work_orders')
    equipments = models.ManyToManyField(Equipment, blank=True, related_name='work_orders')
    assets = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True, blank=True, related_name='work_assets')
    planned_date = models.DateTimeField(null=True, blank=True)
    workers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='work_orders')
    status = models.CharField(max_length=20, default='pendiente',
                              choices=[('pendiente', 'Pendiente'), ('completada', 'Completada')])

    def __str__(self):
        return f"Orden de Trabajo de Proforma {self.proforma.correlative}"
