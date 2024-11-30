from django.shortcuts import render, get_object_or_404
from ClonFlixApp.models import Pelicula, Serie
from unidecode import unidecode

# Para el video de la pagina de inicio
def video_page(request):
    # Ruta del archivo de video
    video_url = '/media/movie_videos/sample_movie.mp4'
    return render(request, 'video.html', {'video_url': video_url})




# Página principal
def index(request):
    peliculas_recientes = Pelicula.objects.order_by('-estreno')[:12]
    series_recientes = Serie.objects.order_by('-estreno')[:12]
    peliculas_mejor_valoradas = Pelicula.objects.filter(calificacion_usuario__isnull=False).order_by('-calificacion_usuario')[:12]
    series_mejor_valoradas = Serie.objects.filter(calificacion_usuario__isnull=False).order_by('-calificacion_usuario')[:12]

    context = {
        'peliculas_recientes': peliculas_recientes,
        'series_recientes': series_recientes,
        'peliculas_mejor_valoradas': peliculas_mejor_valoradas,
        'series_mejor_valoradas': series_mejor_valoradas,
    }
    return render(request, 'ClonFlixApp/index.html', context)


# Novedades más vistas
def novedades_mas_vistas(request):
    novedades_peliculas = Pelicula.objects.order_by('-calificacion_usuario', '-vistas_totales')[:12]
    novedades_series = Serie.objects.order_by('-calificacion_usuario', '-vistas_totales')[:12]
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


# Series recientes
def series_recientes(request):
    series = Serie.objects.all().order_by('-estreno')[:10]
    return render(request, 'ClonFlixApp/series_recientes.html', {'series': series})


# Búsqueda de contenido
def buscar_contenido(request):
    query = request.GET.get('q', '').strip()

    if query:
        normalized_query = unidecode(query).lower()
        peliculas = Pelicula.objects.filter(titulo__icontains=normalized_query)
        series = Serie.objects.filter(titulo__icontains=normalized_query)
    else:
        peliculas = Pelicula.objects.none()
        series = Serie.objects.none()

    sin_resultados = not (peliculas.exists() or series.exists())

    return render(request, 'ClonFlixApp/buscar_resultados.html', {
        'query': query,
        'peliculas': peliculas,
        'series': series,
        'sin_resultados': sin_resultados,
    })


# Detalle de contenido
def detalle_pelicula(request, id):
    pelicula = get_object_or_404(Pelicula, id=id)
    return render(request, 'ClonFlixApp/detalle_pelicula.html', {'pelicula': pelicula})


def detalle_serie(request, id):
    serie = get_object_or_404(Serie, id=id)
    return render(request, 'ClonFlixApp/detalle_serie.html', {'serie': serie})


# Vistas para series y películas
def series_view(request):
    series = Serie.objects.all()
    return render(request, 'ClonFlixApp/series.html', {'series': series})


def peliculas_view(request):
    peliculas = Pelicula.objects.all()
    return render(request, 'ClonFlixApp/peliculas.html', {'peliculas': peliculas})
