from django.db import models

### 📌 General system settings
from django.db import models

class SiteConfig(models.Model):
    primary_logo = models.FileField(
        upload_to="logos/",
        blank=True,
        null=True,
        help_text="Logo principal del sistema"
    )
    secondary_logo = models.FileField(
        upload_to="logos/",
        blank=True,
        null=True,
        help_text="Logo secundario del sistema"
    )

    def __str__(self):
        return "Configuración del Sitio"

    @classmethod
    def get_logos(cls):
        config = cls.objects.first()
        primary_logo = config.primary_logo.url if config and config.primary_logo else "/static/logos/default_primary.svg"
        secondary_logo = config.secondary_logo.url if config and config.secondary_logo else "/static/logos/default_secondary.svg"
        return {"primary_logo": primary_logo, "secondary_logo": secondary_logo}


### 📌 Organizational structure
class Area(models.Model):
    name = models.CharField(max_length=100, unique=True)
    cod = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, blank=True)
    cod = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name} ({self.area.name if self.area else 'Sin área'})"


class Period(models.Model):
    name = models.CharField(max_length=100, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)