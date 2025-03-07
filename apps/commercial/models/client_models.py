from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from core.models import Comment


class Client(models.Model):
    business_name = models.CharField(max_length=255, blank=True, null=True)
    tax_id = models.CharField(max_length=11, unique=True, blank=True, null=True)
    address = models.TextField(default="Direccion")
    department = models.CharField(max_length=100, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    economic_activity = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    condition = models.CharField(max_length=50, blank=True, null=True)
    is_retention_agent = models.BooleanField(default=False)
    workers_number = models.CharField(max_length=50, blank=True, null=True)
    billing_type = models.CharField(max_length=50, blank=True, null=True)
    accounting_type = models.CharField(max_length=50, blank=True, null=True)
    foreign_trade = models.CharField(max_length=50, blank=True, null=True)
    company_type = models.CharField(max_length=100, blank=True, null=True)
    payment_method = models.CharField(max_length=50, default="Contado", choices=[('contado', 'Al contado'), ('credito', 'Credito')])
    comments = GenericRelation(Comment)

    def get_comments(self):
        return self.comments.all()

    def __str__(self):
        return f"{self.business_name} - {self.status}"


class Branch(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="branches")
    name = models.CharField(max_length=255, default="Sucursal")
    address = models.TextField()
    ubigeo = models.CharField(max_length=10, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    is_headquarters = models.BooleanField(default=False)
    sales_advisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        limit_choices_to={'groups__name': 'COMERCIAL'}
    )

    def __str__(self):
        return f"{self.name} ({self.client.business_name})"


class Contact(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="contacts")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="contacts")
    name = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=50, choices=[
        ('billing', 'Responsable de Facturación'),
        ('payment', 'Responsable de Pago'),
        ('compliance', 'Responsable de Conformidad'),
        ('certificate', 'Contacto para Certificado Digital'),
        ('user', 'Usuario del Servicio')
    ])

    def __str__(self):
        return f"{self.name} - {self.role} ({self.client.business_name})"