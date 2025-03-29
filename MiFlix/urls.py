from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # aqui redirigimos a las ruta raiz a MiFlix
    path('', include('MiFlixApp.urls')),

    # Aqui a las de los  usuarios
    path('usuarios/', include('usuarios.urls')),

    # Las de la  administración de django
    path('admin/', admin.site.urls),
]

#  modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
