from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from usuarios.models import UsuarioContenido
from ClonFlixApp.models import Pelicula, Serie
from django.db.models import Q
import random


# Página principal
def index(request):
    peliculas_recientes = Pelicula.objects.all().order_by('-estreno')[:4]
    series_recientes = Serie.objects.all().order_by('-estreno')[:4]

    return render(request, 'ClonFlixApp/index.html', {
        'peliculas_recientes': peliculas_recientes,
        'series_recientes': series_recientes,
    })

def novedades_mas_vistas(request):
    # Selecciona las películas y series con mayor calificación o más vistas
    novedades_peliculas = Pelicula.objects.order_by('-calificacion_usuario', '-vistas_totales')[:8]
    novedades_series = Serie.objects.order_by('-calificacion_usuario', '-vistas_totales')[:8]

    return render(request, 'ClonFlixApp/novedades_mas_vistas.html', {
        'novedades_peliculas': novedades_peliculas,
        'novedades_series': novedades_series,
    })


# Películas por género
def peliculas_por_genero(request, genre):
    peliculas = Pelicula.objects.filter(genero__iexact=genre)
    return render(request, 'ClonFlixApp/peliculas_por_genero.html', {
        'peliculas': peliculas,
        'genero': genre.capitalize(),
    })

def series_recientes(request):
    # Obtiene las series más recientes ordenadas por fecha de estreno
    series = Serie.objects.all().order_by('-estreno')[:10]
    return render(request, 'ClonFlixApp/series_recientes.html', {'series': series})

def buscar_contenido(request):
    query = request.GET.get('q', '').strip()  # Obtén y limpia el término de búsqueda
    peliculas = Pelicula.objects.filter(
        Q(titulo__icontains=query) | Q(genero__icontains=query) | Q(protagonistas__icontains=query)
    )
    series = Serie.objects.filter(
        Q(titulo__icontains=query) | Q(genero__icontains=query) | Q(protagonistas__icontains=query)
    )
    return render(request, 'ClonFlixApp/buscar_resultados.html', {
        'query': query,
        'peliculas': peliculas,
        'series': series,
    })


# Detalle de la película
def detalle_pelicula(request, id):
    pelicula = get_object_or_404(Pelicula, id=id)
    return render(request, 'ClonFlixApp/detalle_pelicula.html', {'pelicula': pelicula})

# Detalle de la serie
def detalle_serie(request, id):
    serie = get_object_or_404(Serie, id=id)
    return render(request, 'ClonFlixApp/detalle_serie.html', {'serie': serie})

# Vistas para series
def series_view(request):
    series = Serie.objects.all()
    return render(request, 'ClonFlixApp/series.html', {'series': series})

# Vistas para películas
def peliculas_view(request):
    peliculas = Pelicula.objects.all()
    return render(request, 'ClonFlixApp/peliculas.html', {'peliculas': peliculas})

# Mi Lista
@login_required
def mi_lista_view(request):
    mi_lista_peliculas = Pelicula.objects.filter(usuarios_pelicula__usuario=request.user)
    mi_lista_series = Serie.objects.filter(usuarios_serie__usuario=request.user)

    return render(request, 'ClonFlixApp/mi_lista.html', {
        'mi_lista_peliculas': mi_lista_peliculas,
        'mi_lista_series': mi_lista_series,
    })

# Marcar contenido como "Añadir a Mi Lista" (Favoritos)
@login_required
def marcar_a_mi_lista(request, contenido_id, tipo):
    if tipo == 'pelicula':
        contenido = get_object_or_404(Pelicula, id=contenido_id)
        usuario_contenido, created = UsuarioContenido.objects.get_or_create(usuario=request.user, pelicula=contenido)
    else:
        contenido = get_object_or_404(Serie, id=contenido_id)
        usuario_contenido, created = UsuarioContenido.objects.get_or_create(usuario=request.user, serie=contenido)

    # Si ya está en la lista, lo elimina; si no, lo agrega.
    if not created:
        usuario_contenido.delete()
    return redirect('detalle_pelicula' if tipo == 'pelicula' else 'detalle_serie', id=contenido.id)
