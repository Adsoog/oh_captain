from django.db import models
from django.conf import settings
from core.models import Area, Period, Department
from apps.commercial.models.client_models import Client
from apps.planning.models.workorder_models import WorkOrder


class Solicitation(models.Model):
    class SolicitationType(models.TextChoices):
        EXIT_TICKET = 'exit_ticket', 'Papeleta de salida'
        EXPENSES = 'expenses', 'Entregas por rendir'
        PETTY_CASH = 'petty_cash', 'Caja chica'
        MOBILITY_SHEET = 'mobility_sheet', 'Planilla de movilidad'
        PERDIEM_REQUEST = 'perdiem_request', 'Solicitud de viáticos'

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
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                 related_name="expenditure_reports")
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, related_name="expenditure_reports")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="expenditure_reports")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='draft')
    work_order = models.ForeignKey(WorkOrder, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='solicitations')
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    solicitation_type = models.CharField(max_length=50, choices=SolicitationType.choices,
                                         default=SolicitationType.PERDIEM_REQUEST)

    def __str__(self):
        return f"{self.get_solicitation_type_display()} - {self.correlative}"


class SolicitationAdvance(models.Model):
    solicitation = models.ForeignKey(Solicitation, related_name='advances', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    deposit_date = models.DateField()
    comments = models.TextField(blank=True, null=True)
    voucher_number = models.CharField(max_length=50, blank=True, null=True, help_text="Número del comprobante")
    voucher_file = models.FileField(upload_to='vouchers/', blank=True, null=True,
                                    help_text="Archivo del comprobante (PDF o imagen)")

    class Meta:
        verbose_name = "Abono"
        verbose_name_plural = "Abonos"


class SolicitationApprovals(models.Model):
    APPROVAL_TYPES = [
        ('employee', 'Empleado'),
        ('manager', 'Gerente'),
        ('rrhh', 'Recursos Humanos'),
        ('finance', 'Finanzas'),
    ]
    solicitation = models.ForeignKey(Solicitation, related_name='approvals', on_delete=models.CASCADE)
    approval_type = models.CharField(max_length=30, choices=APPROVAL_TYPES)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    approved_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.solicitation.correlative} - {self.get_approval_type_display()} by {self.approved_by}"

    class Meta:
        verbose_name = "Aprobación de solicitud"
        verbose_name_plural = "Aprobaciones de solicitud"


class ExitTicket(models.Model):
    solicitation = models.OneToOneField(Solicitation, on_delete=models.CASCADE, related_name="exit_ticket_detail")
    details = models.TextField(blank=True, null=True, help_text="Detalles adicionales para la papeleta de salida.")

    def __str__(self):
        return f"Papeleta de salida - {self.solicitation.correlative}"


class Expenses(models.Model):
    solicitation = models.OneToOneField(Solicitation, on_delete=models.CASCADE, related_name="expenses_detail")
    details = models.TextField(blank=True, null=True, help_text="Detalles adicionales para entregas por rendir.")

    def __str__(self):
        return f"Entrega por rendir - {self.solicitation.correlative}"


class PettyCash(models.Model):
    solicitation = models.OneToOneField(Solicitation, on_delete=models.CASCADE, related_name="petty_cash_detail")
    details = models.TextField(blank=True, null=True, help_text="Detalles adicionales para caja chica.")

    def __str__(self):
        return f"Caja chica - {self.solicitation.correlative}"


class MobilitySheet(models.Model):
    solicitation = models.OneToOneField(Solicitation, on_delete=models.CASCADE, related_name="mobility_sheet_detail")
    details = models.TextField(blank=True, null=True, help_text="Detalles adicionales para planilla de movilidad.")

    def __str__(self):
        return f"Planilla de movilidad - {self.solicitation.correlative}"


class PerdiemRequest(models.Model):
    solicitation = models.OneToOneField(Solicitation, on_delete=models.CASCADE, related_name="perdiem_request_detail")
    details = models.TextField(blank=True, null=True, help_text="Detalles adicionales para solicitud de viáticos.")

    def __str__(self):
        return f"Solicitud de viáticos - {self.solicitation.correlative}"
