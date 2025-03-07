from django.db import models


class Instrument(models.Model):
    name = models.CharField(max_length=255, verbose_name="Instrumento de medición o artefacto", help_text="Nombre del instrumento de medición.")
    discipline = models.CharField(max_length=255, verbose_name="Disciplina / Magnitud", help_text="Seleccione la disciplina o magnitud a la que pertenece el instrumento.")
    subdiscipline = models.CharField(max_length=255, blank=True, null=True, verbose_name="Subdisciplina", help_text="Indique una subdisciplina específica, si aplica.")
    procedure_code = models.CharField(max_length=10, verbose_name="Código del Procedimiento", help_text="Código del procedimiento de calibración o verificación.")
    procedure = models.TextField(verbose_name="Procedimiento", help_text="Descripción del procedimiento utilizado.")
    commercial_area_notes = models.TextField(blank=True, null=True, verbose_name="Notas para el Área Comercial", help_text="Cualquier observación relevante para el área comercial.")
    measurement_range_from = models.CharField(max_length=50, verbose_name="Intervalo de Medida Desde", help_text="Valor mínimo del intervalo de medición.")
    measurement_range_to = models.CharField(max_length=50, verbose_name="Intervalo de Medida Hasta", help_text="Valor máximo del intervalo de medición.")
    indicator_resolution = models.CharField(max_length=50, verbose_name="Resolución del Indicador", help_text="Precisión o resolución del indicador del instrumento.")
    brand = models.CharField(max_length=100, blank=True, null=True, verbose_name="Marca", help_text="Marca del instrumento.")
    model = models.CharField(max_length=100, blank=True, null=True, verbose_name="Modelo", help_text="Modelo del instrumento.")
    expanded_uncertainty = models.CharField(max_length=100, blank=True, null=True, verbose_name="Incertidumbre Expandida", help_text="Nivel de confianza en las mediciones del instrumento.")
    accredited = models.BooleanField(default=False, verbose_name="Acreditado", help_text="Indique si el instrumento está acreditado.")
    accreditation_condition = models.CharField(max_length=100, blank=True, null=True, verbose_name="Condición de Acreditación", help_text="Detalles de la acreditación del instrumento.")
    employed_standards = models.TextField(blank=True, null=True, verbose_name="Patrones Empleados", help_text="Patrones de referencia utilizados.")
    man_hours = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Horas Hombre", help_text="Horas hombre requeridas para el mantenimiento o calibración.")
    necessary_workers = models.IntegerField(default=1)
    calibration_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo de Calibración", help_text="Costo asociado a la calibración del instrumento.")
    verification_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo de Verificación", help_text="Costo asociado a la verificación del instrumento.")
    preventive_maintenance_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo de Mantenimiento Preventivo", blank=True, null=True, help_text="Costo del mantenimiento preventivo.")
    transport_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo de transporte", help_text="Costo del transport del instrumento por km.")
    for_sale = models.BooleanField(default=False, verbose_name="En Venta", help_text="Indique si este instrumento está disponible para la venta.")
    technical_notes = models.TextField(blank=True, null=True, verbose_name="Notas Técnicas", help_text="Notas técnicas relevantes sobre el instrumento.")
    cost_center = models.CharField(max_length=50, verbose_name="Centro de Costos", help_text="Código del centro de costos relacionado con este instrumento.")
    in_arequipa = models.BooleanField(default=False, verbose_name="En Arequipa", help_text="Indique si el instrumento está ubicado en Arequipa.")
    in_lima = models.BooleanField(default=False, verbose_name="En Lima", help_text="Indique si el instrumento está ubicado en Lima.")
    considerations = models.CharField(max_length=255, blank=True, null=True, verbose_name="Consideraciones", help_text="Condiciones para el servicio del instrumento.")

    def __str__(self):
        return f"{self.name}"