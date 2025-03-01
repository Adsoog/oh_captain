from django.db import models

class SiteConfig(models.Model):
    primary_logo = models.ImageField(upload_to="logos/", blank=True, null=True, help_text="Logo principal del sistema")
    secondary_logo = models.ImageField(upload_to="logos/", blank=True, null=True, help_text="Logo secundario del sistema")

    def __str__(self):
        return "Configuración del Sitio"

    @classmethod
    def get_logos(cls):
        """ Retorna las URLs de los logos primario y secundario """
        config = cls.objects.first()
        primary_logo = config.primary_logo.url if config and config.primary_logo else "/static/logos/default_primary.svg"
        secondary_logo = config.secondary_logo.url if config and config.secondary_logo else "/static/logos/default_secondary.svg"
        return {"primary_logo": primary_logo, "secondary_logo": secondary_logo}
        