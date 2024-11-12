from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Página de inicio

    # Rutas para películas
    path('peliculas/', views.peliculas_view, name='peliculas'),  # Página de películas
    path('peliculas/<int:id>/', views.detalle_pelicula, name='detalle_pelicula'),  # Detalles de una película específica
    path('peliculas/<int:id>/favorito/', views.marcar_favorito, name='marcar_favorito'),  # Marcar como favorito
    path('peliculas/<int:id>/visto/', views.marcar_visto, name='marcar_visto'),  # Marcar como visto
    path('genero/<str:genre>/', views.peliculas_por_genero, name='peliculas_por_genero'),  # Películas por género
    path('buscar/', views.buscar_peliculas, name='buscar_peliculas'),  # Búsqueda de películas

    # Rutas para series
    path('series/', views.series_view, name='series'),  # Página de series
    path('series/<int:id>/', views.detalle_serie, name='detalle_serie'),  # Detalles de una serie específica
    path('series-recientes/', views.series_recientes, name='series_recientes'),  # Ruta para 'Series Recientes'

    # Rutas para secciones de contenido
    path('novedades-mas-vistas/', views.novedades_mas_vistas, name='novedades_mas_vistas'),  # Página de novedades
    path('recomendacion-usuarios/', views.recomendacion_usuarios, name='recomendacion_usuarios'),  # Página de recomendaciones

    # Ruta para 'Mi Lista' del usuario
    path('mi_lista/', views.mi_lista_view, name='mi_lista'),

    # Ruta de logout
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),  # Redirección a la página de inicio después de cerrar sesión
]
