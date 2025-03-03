from django.db import models
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
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="expenditure_reports")
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, related_name="expenditure_reports")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="expenditure_reports")
    employee_approval = models.BooleanField(default=False)
    manager_approval = models.BooleanField(default=False)
    rrhh_approval = models.BooleanField(default=False)
    finance_approval = models.BooleanField(default=False)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='draft')
    oti = models.CharField(max_length=50, null=True, blank=True)
    client = models.CharField(max_length=50, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    days = models.IntegerField(null=True, blank=True)

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

class PerDiemSettlementBill(models.Model):
    BILL_TYPE_CHOICES = [
        ('FACTURA', 'Factura'),
        ('BOLETA', 'Boleta'),
        ('RECIBO', 'Recibo'),
        ('TICKET', 'Ticket'),
        ('RECIBOHONORARIOS', 'Recibo por honorarios'),
        ('PLANILLA_MOVILIDAD', 'Planilla movilidad'),
    ]
    BILL_CLASS_CHOICES = [
        ('ALIMENTACION', 'Alimentacion'),
        ('HOSPEDAJE', 'Hospedaje'),
        ('MOVILIDAD', 'Movilidad'),
        ('PEAJE', 'Peaje'),
        ('PASAJES', 'Pasajes'),
        ('OTROS', 'Otros'),
    ]

    request_bill = models.ForeignKey(PerDiemSettlement, on_delete=models.CASCADE, related_name='service_bills', null=True, blank=True)
    bill_image = models.FileField(upload_to="bills/", null=True, blank=True)
    bill_ruc = models.BigIntegerField(null=True, blank=True)
    bill_emisor = models.CharField(max_length=100, null=True, blank=True)
    bill_number = models.CharField(max_length=50, null=True, blank=True)
    bill_series = models.CharField(max_length=50, null=True, blank=True)
    bill_date = models.DateField(null=True, blank=True)
    bill_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bill_details = models.CharField(max_length=150, null=True, blank=True)
    bill_type = models.CharField(max_length=20, choices=BILL_TYPE_CHOICES, null=True, blank=True)
    bill_class = models.CharField(max_length=20, choices=BILL_CLASS_CHOICES, null=True, blank=True)
    bill_is_valid = models.BooleanField(default=False)
    bill_is_valid_reason = models.CharField(max_length=60, default="Por revisar", null=True, blank=True)
    is_active = models.CharField(max_length=50, null=True, blank=True)
    is_found = models.CharField(max_length=50, null=True, blank=True)
    skip_signal = False
    mobility_sheet = models.ForeignKey(
        MobilityExpenseSheet,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='linked_bills',
        verbose_name="Planilla de movilidad"
    )

    def __str__(self):
        return f"Factura {self.bill_number} de {self.bill_total} soles"

    class Meta:
        verbose_name = "Comprobante de liquidacion"
        verbose_name_plural = "Comprobantes de liquidaciones"

class SignatureLog(models.Model):
    SIGNATURE_TYPES = [
        ('applicant', 'Applicant'),
        ('supervisor', 'Supervisor'),
        ('accounting', 'Accounting'),
        ('settlement_user', 'Settlement User Approval'),
        ('settlement_supervisor', 'Settlement Supervisor Approval'),
    ]

    request_service = models.ForeignKey('PerDiemRequest', on_delete=models.CASCADE, null=True, blank=True, related_name='signature_logs')
    settlement = models.ForeignKey('PerDiemSettlement', on_delete=models.CASCADE, null=True, blank=True, related_name='signature_logs')
    mobility_sheet = models.ForeignKey('MobilityExpenseSheet', on_delete=models.CASCADE, null=True, blank=True, related_name='signature_logs')
    signature_type = models.CharField(max_length=35, choices=SIGNATURE_TYPES)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    signed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        target = self.request_service or self.settlement
        return f"{self.signature_type} - {self.user} for {target} at {self.signed_at}"

    class Meta:
        verbose_name = "Historial de aprobacion"
        verbose_name_plural = "Historial de aprobaciones"


class RequestItem(models.Model):
    DOC_TYPE_CHOICES = [
        ('F', 'Factura'),
        ('RH', 'Recibo por Honorario'),
        ('BOL', 'Boleta'),
    ]
    TRANSPORT_CHOICES = [
        ('TAXI', 'Taxi'),
        ('BUS', 'Transporte colectivo'),
    ]
    request = models.ForeignKey(Request,on_delete=models.CASCADE,related_name='item')
    date = models.DateField(blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255, null=True, blank=True)
    payment_method = models.CharField(max_length=20,choices=[('cash', 'Efectivo'), ('transfer', 'Transferencia')],default='cash')
    receipt_file = models.FileField(upload_to='expenditure_receipts/', null=True, blank=True)
    ruc_or_dni = models.CharField(max_length=20)  # RUC o DNI del proveedor
    provider_name = models.CharField(max_length=100, default='No encontrado')
    doc_type = models.CharField(max_length=10, choices=DOC_TYPE_CHOICES)  # Tipo de documento
    document = models.CharField(max_length=50)  # Documento (Ej: E001-12524)
    #cost_center = models.ForeignKey(CostCenter, on_delete=models.SET_NULL, null=True, related_name="expenditure_details")  # Centro de costo
    amount = models.DecimalField(max_digits=12, decimal_places=2)  # Monto
    reason = models.CharField(max_length=150, null=True, blank=True)
    route = models.CharField(max_length=255, null=True, blank=True)
    transport_mode = models.CharField(max_length=100, choices=TRANSPORT_CHOICES, null=True, blank=True)
    daily_amount = models.DecimalField(max_digits=10, decimal_places=2)
    approver_signature = models.BooleanField(default=False)