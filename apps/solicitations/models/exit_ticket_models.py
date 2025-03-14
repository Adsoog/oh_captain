from django.db import models
from apps.solicitations.models.solicitation_models import Solicitation


class ExitTicket(models.Model):
    solicitation = models.OneToOneField(Solicitation, on_delete=models.CASCADE, related_name="exit_ticket_detail")
    details = models.TextField(blank=True, null=True, help_text="Detalles adicionales para la papeleta de salida.")

    def __str__(self):
        return f"Papeleta de salida - {self.solicitation.correlative}"
