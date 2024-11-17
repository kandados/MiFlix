from django.contrib import admin
from django.apps import apps

Pelicula = apps.get_model('ClonFlixApp', 'Pelicula')
Serie = apps.get_model('ClonFlixApp', 'Serie')

@admin.register(Pelicula)
class PeliculaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'estreno', 'genero', 'vistas_totales')
    search_fields = ('titulo', 'director', 'protagonistas')


@admin.register(Serie)
class SerieAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'estreno', 'genero', 'temporadas_totales', 'capitulos_totales')
    search_fields = ('titulo', 'director', 'protagonistas')
