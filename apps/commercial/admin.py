from apps.commercial.models.proforma_models import Service
from django.contrib import admin


# Register your models here.

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('tipo_servicio', 'valor_bruto')
    list_filter = ('type',)
    search_fields = ('type',)
    ordering = ('type',)

    def tipo_servicio(self, obj):
        """Muestra la versión legible del tipo de servicio"""
        return obj.get_type_display()

    tipo_servicio.short_description = 'Tipo de Servicio'

    def valor_bruto(self, obj):
        """Muestra el valor crudo del campo type"""
        return obj.type

    valor_bruto.short_description = 'Valor en BD'

    # Opcional: Para mostrar los choices como radio buttons en el formulario
    radio_fields = {'type': admin.HORIZONTAL}
