from django.urls import include, path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'usuarios'

urlpatterns = [
    #Incluimos las urls de MiFlixApp
    path('', include('MiFlixApp.urls')),
    # Autenticación
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('inicio-personalizado/', views.inicio_personalizado, name='inicio_personalizado'),

    # Panel de administración
    path('panel-admin/', views.panel_admin, name='panel_admin'),
    path('gestion-usuarios/', views.gestion_usuarios, name='gestion_usuarios'),
    path('gestion-usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('gestion-usuarios/editar/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('gestion-usuarios/eliminar/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('estadisticas-usuario/<int:usuario_id>/', views.estadisticas_usuario_admin, name='estadisticas_usuario'),
    path('graficas-y-stats/', views.graficas_y_stats, name='graficas_y_stats'),

    # Gestión de Contenidos
    path('gestion-contenidos/', views.gestion_contenidos, name='gestion_contenidos'),
    path('gestion-contenidos/crear-pelicula/', views.crear_pelicula, name='crear_pelicula'),
    path('editar-pelicula/<int:pelicula_id>/', views.editar_pelicula, name='editar_pelicula'),
    path('eliminar-pelicula/<int:pelicula_id>/', views.eliminar_pelicula, name='eliminar_pelicula'),
    path('crear-serie/', views.crear_serie, name='crear_serie'),
    path('editar-serie/<int:serie_id>/', views.editar_serie, name='editar_serie'),
    path('eliminar-serie/<int:serie_id>/', views.eliminar_serie, name='eliminar_serie'),

    # Panel de usuario
    path('panel-usuario/', views.panel_usuario, name='panel_usuario'),
    path('favoritos/', views.favoritas_view, name='favoritos'),
    path('ya-vistas/', views.ya_vistas_view, name='ya_vistas'),
    path('estadisticas-usuario/', views.estadisticas_usuario, name='estadisticas_usuario'),

    # Marcar como favorita , vista o calificar
    path('contenido/<int:contenido_id>/favorito/<str:tipo>/', views.marcar_favorito, name='marcar_favorito'),
    path('contenido/<int:contenido_id>/visto/<str:tipo>/', views.marcar_como_visto, name='marcar_como_visto'),

    # Gráficas y estadísticas (admin)
    path('graficas-y-stats/', views.graficas_y_stats, name='graficas_y_stats'),
    path('estadisticas-usuario/<int:usuario_id>/', views.estadisticas_usuario_admin, name='estadisticas_usuario_admin'),

]
