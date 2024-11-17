from django.urls import path
from . import views

app_name = 'ClonFlixApp'

urlpatterns = [
    # Página principal
    path('', views.index, name='index'),

    # Rutas de películas
    path('peliculas/', views.peliculas_view, name='peliculas'),
    path('detalle_pelicula/<int:id>/', views.detalle_pelicula, name='detalle_pelicula'),
    path('peliculas/<int:contenido_id>/accion/<str:accion>/', views.marcar_a_mi_lista, {'tipo': 'pelicula'}, name='accion_pelicula'),

    # Rutas de series
    path('series/', views.series_view, name='series'),
    path('detalle_serie/<int:id>/', views.detalle_serie, name='detalle_serie'),
    path('series/<int:contenido_id>/accion/<str:accion>/', views.marcar_a_mi_lista, {'tipo': 'serie'}, name='accion_serie'),

    # Categorías y búsqueda
    path('genero/<str:genre>/', views.peliculas_por_genero, name='peliculas_por_genero'),
    path('buscar/', views.buscar_contenido, name='buscar_contenido'),

    # Novedades y series recientes
    path('novedades-mas-vistas/', views.novedades_mas_vistas, name='novedades_mas_vistas'),
    path('series-recientes/', views.series_recientes, name='series_recientes'),

    # Mi Lista
    path('mi_lista/', views.mi_lista_view, name='mi_lista'),
]
