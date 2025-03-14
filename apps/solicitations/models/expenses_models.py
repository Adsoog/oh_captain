from django.db import models
from apps.solicitations.models.solicitation_models import Solicitation


class Expenses(models.Model):
    solicitation = models.OneToOneField(Solicitation, on_delete=models.CASCADE, related_name="expense")
    details = models.TextField(blank=True, null=True,)

    def __str__(self):
        return f"Papeleta de salida - {self.solicitation.correlative}"
