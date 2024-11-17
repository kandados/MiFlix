from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'usuarios'

urlpatterns = [
    # Autenticación
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='usuarios:login'), name='logout'),

    # Paneles de acceso
    path('panel-admin/', views.panel_admin, name='panel_admin'),
    path('panel-usuario/', views.panel_usuario, name='panel_usuario'),

    # Gestión de usuarios
    path('gestion-usuarios/', views.gestion_usuarios, name='gestion_usuarios'),
    path('gestion-usuarios/editar/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('gestion-usuarios/eliminar/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),


    # Interacción con contenido
    path('contenido/<int:contenido_id>/favorito/<str:tipo>/', views.marcar_favorito, name='marcar_favorito'),
    path('contenido/<int:contenido_id>/mi-lista/<str:tipo>/', views.agregar_a_mi_lista, name='agregar_a_mi_lista'),

    # Página de inicio personalizada
    path('', views.inicio, name='index'),
]
