from django.db import models
from django.core.validators import FileExtensionValidator


class ExpenseItem(models.Model):
    DOC_TYPE_CHOICES = [
        ('F', 'Factura'),
        ('RH', 'Recibo por Honorario'),
        ('BOL', 'Boleta'),
    ]

    currency = models.CharField(max_length=10, choices=[("SOLES", "Soles"), ("USD", "Dólares")], default="SOLES")
    total_requested = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    money_received = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    balance_to_return = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    number = models.PositiveIntegerField(null=True, blank=True)  # Número en la lista
    date = models.DateField()  # Fecha del gasto
    ruc_or_dni = models.CharField(max_length=20)  # RUC o DNI del proveedor
    provider_name = models.CharField(max_length=100, default='No encontrado')  # Nombre del proveedor
    description = models.CharField(max_length=250)  # Descripción del gasto
    doc_type = models.CharField(max_length=10, choices=DOC_TYPE_CHOICES)  # Tipo de documento
    document = models.CharField(max_length=50)  # Documento (Ej: E001-12524)
    amount = models.DecimalField(max_digits=12, decimal_places=2)  # Monto
    attachment = models.FileField(
        upload_to='expenditure_details/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])]
    )

    def __str__(self):
        return f"{self.provider_name} - {self.description} - S/ {self.amount}"
