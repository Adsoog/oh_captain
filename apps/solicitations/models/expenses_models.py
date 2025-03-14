from django.db import models
from core.models import CostCenter
from django.core.validators import FileExtensionValidator
from apps.solicitations.models.solicitation_models import Solicitation


class Expense(models.Model):
    solicitation = models.OneToOneField(Solicitation, on_delete=models.CASCADE, related_name="expense")
    total_requested = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_items = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    correlative = models.CharField(max_length=20, unique=True, null=True, blank=True)


class ExpenseItem(models.Model):
    DOC_TYPE_CHOICES = [
        ('F', 'Factura'),
        ('RH', 'Recibo por Honorario'),
        ('BOL', 'Boleta'),
    ]
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name="items")
    number = models.PositiveIntegerField(null=True, blank=True)
    date = models.DateField()
    ruc_or_dni = models.CharField(max_length=20)
    provider_name = models.CharField(max_length=100, default='No encontrado')
    description = models.CharField(max_length=250)
    doc_type = models.CharField(max_length=10, choices=DOC_TYPE_CHOICES)
    doc = models.CharField(max_length=50)
    cost_center = models.ForeignKey(CostCenter, on_delete=models.SET_NULL, null=True,
                                    related_name="expenditure_details")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    file = models.FileField(
        upload_to='expenditure_details/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])]
    )

    def __str__(self):
        return f"{self.provider_name} - {self.description} - S/ {self.amount}"
