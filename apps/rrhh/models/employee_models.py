from django.db import models
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey
from core.models import Department, Area


class Employee(MPTTModel):  # Cambio a MPTTModel
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employee_profile",
        verbose_name="Usuario"
    )

    # Personal info
    first_name = models.CharField("Primer nombre", max_length=50)
    second_name = models.CharField("Segundo nombre", max_length=50, blank=True, null=True)
    paternal_surname = models.CharField("Apellido paterno", max_length=50)
    maternal_surname = models.CharField("Apellido materno", max_length=50, blank=True, null=True)
    dni = models.CharField("DNI", max_length=20, unique=True)
    date_of_birth = models.DateField("Fecha de nacimiento", blank=True, null=True)
    gender = models.CharField(
        "Género",
        max_length=10,
        choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')],
        blank=True,
        null=True
    )
    blood_type = models.CharField("Tipo de sangre", max_length=3, blank=True, null=True)
    controlled = models.BooleanField("Controlado", default=False, help_text="¿Cuenta con registro de control sanitario?")
    marital_status = models.CharField(
        "Estado civil",
        max_length=20,
        choices=[('single', 'Soltero'), ('married', 'Casado'), ('divorced', 'Divorciado'), ('widowed', 'Viudo')],
        blank=True,
        null=True
    )
    address = models.CharField("Dirección", max_length=255, blank=True, null=True)
    phone_number = models.CharField("Teléfono", max_length=20, blank=True, null=True)
    emergency_contact = models.CharField("Contacto de emergencia", max_length=100, blank=True, null=True)

    # Datos laborales
    position = models.CharField(max_length=70, null=True, blank=True)
    headquarters = models.CharField(max_length=50, null=True, blank=True)
    hire_date = models.DateField("Fecha de contratación", blank=True, null=True)
    job_title = models.CharField("Cargo", max_length=100, blank=True, null=True)
    salary = models.DecimalField("Salario", max_digits=10, decimal_places=2, blank=True, null=True)
    contract_type = models.CharField(
        "Tipo de contrato",
        max_length=50,
        choices=[('permanent', 'Permanente'), ('temporary', 'Temporal')],
        blank=True,
        null=True
    )

    parent = TreeForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',  # o 'subordinates', como prefieras
        verbose_name='Padre'
    )

    profession = models.CharField("Profesión", max_length=100, blank=True, null=True)

    # Relaciones con otras entidades
    area = models.ForeignKey(
        Area,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Área"
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Departamento"
    )
    additional_info = models.TextField("Información adicional", blank=True, null=True)

    class MPTTMeta:
        pass
        #order_insertion_by = ['first_name']

    def __str__(self):
        nombre = self.first_name
        apellido = self.paternal_surname
        cargo = self.job_title or "Sin cargo"
        return f"{nombre} {apellido} - {cargo}"
