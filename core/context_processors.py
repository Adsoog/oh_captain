from django.core.cache import cache
from .models import SiteConfig

def get_site_logos(request):
    """Provides the primary and secondary logo URLs for templates."""
    config = SiteConfig.objects.first()
    return {
        "primary_logo": config.primary_logo.url if config and config.primary_logo else "/static/logos/default_primary.svg",
        "secondary_logo": config.secondary_logo.url if config and config.secondary_logo else "/static/logos/default_secondary.svg",
    }