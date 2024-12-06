from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ClonFlixApp.models import Pelicula, Serie  # Asegúrate de tener UsuarioContenido definido en tus modelos
from unidecode import unidecode
from usuarios.models import UsuarioContenido
from django.db.models import Avg

# Para el video de la pagina de inicio
def video_page(request):
    # Ruta del archivo de video
    video_url = '/media/movie_videos/sample_movie.mp4'
    return render(request, 'video.html', {'video_url': video_url})


# Página principal
def index(request):
    # Película destacada (Pelicula asociada al video de inicio)
    pelicula_destacada = Pelicula.objects.filter(id=108).first()
    if pelicula_destacada:
        pelicula_destacada.descripcion_breve = "La insólita amistad entre el adolescente vikingo Hipo y su fiel compañero dragón, el Furia Nocturna Desdentao."

    # Lista de peliculas y series ya existentes
    peliculas_recientes = Pelicula.objects.order_by('-estreno')[:12]
    series_recientes = Serie.objects.order_by('-estreno')[:12]
    peliculas_mejor_valoradas = Pelicula.objects.filter(calificacion_usuario__isnull=False).order_by('-calificacion_usuario')[:12]
    series_mejor_valoradas = Serie.objects.filter(calificacion_usuario__isnull=False).order_by('-calificacion_usuario')[:12]

    context = {
        'pelicula_destacada': pelicula_destacada,
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

    # Calcular la calificación promedio de la película
    promedio_calificacion = UsuarioContenido.objects.filter(
        pelicula=pelicula,
        calificacion__isnull=False
    ).aggregate(promedio=Avg('calificacion'))['promedio']

    # Obtener la calificación del usuario actual, si existe
    tu_calificacion = None
    if request.user.is_authenticated:
        usuario_contenido = UsuarioContenido.objects.filter(
            usuario=request.user,
            pelicula=pelicula
        ).first()
        if usuario_contenido:
            tu_calificacion = usuario_contenido.calificacion

    return render(request, 'ClonFlixApp/detalle_pelicula.html', {
        'pelicula': pelicula,
        'promedio_calificacion': round(promedio_calificacion, 1) if promedio_calificacion else None,
        'tu_calificacion': tu_calificacion,
    })


def detalle_serie(request, id):
    serie = get_object_or_404(Serie, id=id)

    # Calcular la calificación promedio de la serie
    promedio_calificacion = UsuarioContenido.objects.filter(
        serie=serie,
        calificacion__isnull=False
    ).aggregate(promedio=Avg('calificacion'))['promedio']

    # Obtener la calificación del usuario actual, si existe
    tu_calificacion = None
    if request.user.is_authenticated:
        usuario_contenido = UsuarioContenido.objects.filter(
            usuario=request.user,
            serie=serie
        ).first()
        if usuario_contenido:
            tu_calificacion = usuario_contenido.calificacion

    return render(request, 'ClonFlixApp/detalle_serie.html', {
        'serie': serie,
        'promedio_calificacion': round(promedio_calificacion, 1) if promedio_calificacion else None,
        'tu_calificacion': tu_calificacion,
    })


# Vistas para series y películas
def series_view(request):
    series = Serie.objects.all()
    return render(request, 'ClonFlixApp/series.html', {'series': series})


def peliculas_view(request):
    peliculas = Pelicula.objects.all()
    return render(request, 'ClonFlixApp/peliculas.html', {'peliculas': peliculas})


# Calificar contenido
@login_required
def calificar_contenido(request, contenido_id, tipo):
    if request.method == 'POST':
        calificacion = request.POST.get('calificacion')
        if not calificacion:
            messages.error(request, "Debes ingresar una calificación.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        try:
            calificacion = float(calificacion)
            if calificacion < 1 or calificacion > 10:
                messages.error(request, "La calificación debe estar entre 1 y 10.")
                return redirect(request.META.get('HTTP_REFERER', '/'))
        except ValueError:
            messages.error(request, "La calificación debe ser un número válido.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        if tipo == 'pelicula':
            contenido = get_object_or_404(Pelicula, id=contenido_id)
        else:
            contenido = get_object_or_404(Serie, id=contenido_id)

        usuario_contenido, _ = UsuarioContenido.objects.get_or_create(
            usuario=request.user,
            pelicula=contenido if tipo == 'pelicula' else None,
            serie=contenido if tipo == 'serie' else None,
        )
        usuario_contenido.calificacion = calificacion
        usuario_contenido.save()

        messages.success(request, f"Calificación registrada para {contenido.titulo}.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    elif request.method == 'GET':
        if tipo == 'pelicula':
            contenido = get_object_or_404(Pelicula, id=contenido_id)
        else:
            contenido = get_object_or_404(Serie, id=contenido_id)
        return render(request, 'ClonFlixApp/calificar_contenido.html', {'contenido': contenido, 'tipo': tipo})


    return HttpResponseNotAllowed(['GET', 'POST'])