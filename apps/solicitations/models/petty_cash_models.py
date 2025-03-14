from django.db import models
from apps.solicitations.models.solicitation_models import Solicitation


class PettyCash(models.Model):
    solicitation = models.OneToOneField(Solicitation, on_delete=models.CASCADE, related_name="petty_cash_detail")
    details = models.TextField(blank=True, null=True, help_text="Detalles adicionales para caja chica.")

    def __str__(self):
        return f"Caja chica - {self.solicitation.correlative}"
