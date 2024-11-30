from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Redirigir a las rutas de la aplicación principal
    path('', include('ClonFlixApp.urls')),

    # Rutas de usuarios
    path('usuarios/', include('usuarios.urls')),

    # Administración
    path('admin/', admin.site.urls),
]

# Configuración de archivos estáticos y multimedia en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
