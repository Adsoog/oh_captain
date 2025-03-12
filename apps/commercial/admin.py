from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.commercial.models.proforma_models import Service, Proforma


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


@admin.register(Proforma)
class ProformaAdmin(ModelAdmin):
    list_display = ('correlative', 'client', 'status')
    list_filter = ('status',)
    actions = ['marcar_como_aceptada']

    def marcar_como_aceptada(self, request, queryset):
        updated_count = 0
        for proforma in queryset:
            proforma.status = 'accepted'
            proforma.save()  # Esto dispara la señal post_save
            updated_count += 1
        self.message_user(request, f"{updated_count} proformas marcadas como aceptadas.")

    marcar_como_aceptada.short_description = "Marcar como Aceptada"
