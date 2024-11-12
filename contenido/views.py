from django.shortcuts import render

# Create your views here.
# contenido/views.py

from contenido.models import Contenido
from usuarios.models import UsuarioContenido

def peliculas_view(request):
    peliculas = Contenido.objects.filter(tipo='pelicula')
    # resto de la vista...

def series_view(request):
    series = Contenido.objects.filter(tipo='serie')
    # resto de la vista...

# Asegúrate de que todas las vistas que antes usaban Movie ahora usan Contenido
