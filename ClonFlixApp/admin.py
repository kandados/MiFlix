

from django.contrib import admin
from .models import Pelicula, Serie

@admin.register(Pelicula)
class PeliculaAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'estreno', 'genero', 'director', 'duracion', 'calificacion_usuario', 'vistas_totales')
    search_fields = ('titulo', 'genero', 'director', 'sinopsis')
    list_filter = ('genero', 'estreno')

@admin.register(Serie)
class SerieAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'estreno', 'genero', 'director', 'temporadas_totales', 'capitulos_totales', 'calificacion_usuario', 'vistas_totales')
    search_fields = ('titulo', 'genero', 'director', 'sinopsis')
    list_filter = ('genero', 'estreno')
