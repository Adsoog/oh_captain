from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('core/', include('core.urls')),
    # apps urls
    path('', include('apps.home.urls')),
    path('rrhh/', include('apps.rrhh.urls')),
    path('supply/', include('apps.supply.urls')),
    path('account/', include('apps.accounts.urls')),
    path('planning/', include('apps.planning.urls')),
    path('commercial/', include('apps.commercial.urls')),
    path('solicitations/', include('apps.solicitations.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
