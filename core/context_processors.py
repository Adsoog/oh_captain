from django.core.cache import cache
from .models import SiteConfig

def get_site_logos(request):
    """ Context processor para obtener los logos principal y secundario """
    logos = cache.get("site_logos")
    if not logos:
        logos = SiteConfig.get_logos()
        cache.set("site_logos", logos, 3600)
    return logos
