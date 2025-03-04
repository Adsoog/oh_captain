from django.db import models
from django.conf import settings
from core.models import Area, Period, Department


class Request(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Borrador'),
        ('created', 'Creada'),
        ('approved', 'Aprobada'),
        ('approved_by_accounting', 'V°B° de Contabilidad'),
        ('rendered', 'Rendida'),
        ('rejected', 'Rechazada'),
    ]
    correlative = models.CharField(max_length=50, null=True, blank=True)
    requested_at = models.DateField(null=True, blank=True)
    period = models.ForeignKey(Period, on_delete=models.SET_NULL, null=True, blank=True)
    reason = models.CharField(max_length=255)
    employee = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, null=True, related_name="expenditure_reports")
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, related_name="expenditure_reports")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="expenditure_reports")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='draft')
    oti = models.CharField(max_length=50, null=True, blank=True)
    client = models.CharField(max_length=50, null=True, blank=True)


class RequestAdvance(models.Model):
    request = models.ForeignKey(Request, related_name='advances', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    deposit_date = models.DateField()
    comments = models.TextField(blank=True, null=True)
    voucher_number = models.CharField(max_length=50, blank=True, null=True, help_text="Número del comprobante")
    voucher_file = models.FileField(upload_to='vouchers/', blank=True, null=True, help_text="Archivo del comprobante (PDF o imagen)")

    class Meta:
        verbose_name = "Abono"
        verbose_name_plural = "Abonos"


class RequestApprovals(models.Model):
    APPROVAL_TYPES = [
        ('employee', 'Empleado'),
        ('manager', 'Gerente'),
        ('rrhh', 'Recursos Humanos'),
        ('finance', 'Finanzas'),
    ]
    request = models.ForeignKey(Request, related_name='approvals', on_delete=models.CASCADE)
    approval_type = models.CharField(max_length=30, choices=APPROVAL_TYPES)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    approved_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.request.correlative} - {self.get_approval_type_display()} by {self.approved_by}"

    class Meta:
        verbose_name = "Aprobación de solicitud"
        verbose_name_plural = "Aprobaciones de solicitud"