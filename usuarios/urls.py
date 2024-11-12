from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # Rutas de autenticación
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Paneles de acceso
    path('panel-admin/', views.panel_admin, name='panel_admin'),
    path('panel-usuario/', views.panel_usuario, name='panel_usuario'),

    # Rutas de administración (solo para administradores)
    path('gestion-usuarios/', views.gestion_usuarios, name='gestion_usuarios'),
    path('gestion-usuarios/editar/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('gestion-usuarios/eliminar/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('gestion-contenido/', views.gestion_contenido, name='gestion_contenido'),
    path('gestion-contenido/crear/', views.crear_contenido, name='crear_contenido'),
    path('gestion-contenido/editar/<int:contenido_id>/', views.editar_contenido, name='editar_contenido'),
    path('gestion-contenido/eliminar/<int:contenido_id>/', views.eliminar_contenido, name='eliminar_contenido'),

    # Moderación y estadísticas
    path('ver-estadisticas/', views.ver_estadisticas, name='ver_estadisticas'),

    # Funciones adicionales para el panel de usuario
    path('favoritos/', views.favoritos, name='favoritos'),
    path('historial/', views.historial, name='historial'),
    path('explorar/', views.explorar, name='explorar'),
    path('inicio/', views.inicio_personalizado, name='inicio_personalizado'),

    # Opciones de marcado de contenido (favorito, visto, ver más tarde, y puntuación)
    path('contenido/<int:contenido_id>/favorito/', views.marcar_favorito, name='marcar_favorito'),
    path('contenido/<int:contenido_id>/visto/', views.marcar_visto, name='marcar_visto'),
    path('contenido/<int:contenido_id>/ver-mas-tarde/', views.marcar_ver_mas_tarde, name='marcar_ver_mas_tarde'),
    path('contenido/<int:contenido_id>/puntuar/', views.puntuar_contenido, name='puntuar_contenido'),

    # Página de inicio
    path('', views.inicio, name='index'),
]



