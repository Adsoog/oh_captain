# admin.py
from django.contrib import admin
from django.utils.safestring import mark_safe
from unfold.admin import ModelAdmin
from .models import SiteConfig

@admin.register(SiteConfig)
class SiteConfigAdmin(ModelAdmin):
    list_display = ("id", "primary_logo_preview", "secondary_logo_preview")
    fields = ("primary_logo", "secondary_logo", "primary_logo_preview", "secondary_logo_preview")
    readonly_fields = ("primary_logo_preview", "secondary_logo_preview")

    def primary_logo_preview(self, obj):
        if obj.primary_logo:
            return mark_safe(f'<img src="{obj.primary_logo.url}" style="height: 50px;">')
        return "No asignado"
    primary_logo_preview.short_description = "Logo Principal"

    def secondary_logo_preview(self, obj):
        if obj.secondary_logo:
            return mark_safe(f'<img src="{obj.secondary_logo.url}" style="height: 50px;">')
        return "No asignado"
    secondary_logo_preview.short_description = "Logo Secundario"
    