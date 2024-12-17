from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ClonFlixApp.models import Pelicula, Serie  # Asegúrate de tener UsuarioContenido definido en tus modelos
from unidecode import unidecode
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from usuarios.models import UsuarioPelicula, UsuarioContenido
from ClonFlixApp.models import Pelicula
from usuarios.models import UsuarioContenido
from django.db.models import Avg
from django.db.models import Count
from usuarios.models import UsuarioPelicula, UsuarioSerie


# Para el video de la pagina de inicio
def video_page(request):
    # Ruta del archivo de video
    video_url = '/media/movie_videos/sample_movie.mp4'
    return render(request, 'video.html', {'video_url': video_url})


from django.shortcuts import render, get_object_or_404
from ClonFlixApp.models import Pelicula, Serie

# Página principal
def index(request):
    # Película destacada
    pelicula_destacada = Pelicula.objects.filter(id=108).first()
    if pelicula_destacada:
        pelicula_destacada.descripcion_breve = "La insólita amistad entre el adolescente vikingo Hipo y su fiel compañero dragón, el Furia Nocturna Desdentao."

    # Películas y series
    peliculas_recientes = Pelicula.objects.order_by('-id')[:12]  # Basado en el orden de creación (id más reciente).
    series_recientes = Serie.objects.order_by('-id')[:12]  # Basado en el orden de creación.
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
    # Películas más vistas
    novedades_peliculas = Pelicula.objects.order_by('-vistas_totales', '-calificacion_usuario', 'titulo')[:12]

    # Series más vistas
    novedades_series = Serie.objects.order_by('-vistas_totales', '-calificacion_usuario', 'titulo')[:12]

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

    promedio_calificacion = UsuarioContenido.objects.filter(
        pelicula=pelicula,
        calificacion__isnull=False
    ).aggregate(promedio=Avg('calificacion'))['promedio']

    tu_calificacion = None
    es_favorito = False
    es_visto = False
    ya_calificado = False  # Nuevo

    if request.user.is_authenticated:
        usuario_contenido = UsuarioContenido.objects.filter(
            usuario=request.user,
            pelicula=pelicula
        ).first()

        if usuario_contenido:
            tu_calificacion = usuario_contenido.calificacion
            es_favorito = usuario_contenido.favorito
            es_visto = usuario_contenido.visto
            ya_calificado = usuario_contenido.calificacion is not None  # Actualizamos aquí

    return render(request, 'ClonFlixApp/detalle_pelicula.html', {
        'pelicula': pelicula,
        'promedio_calificacion': round(promedio_calificacion, 1) if promedio_calificacion else None,
        'tu_calificacion': tu_calificacion,
        'es_favorito': es_favorito,
        'es_visto': es_visto,
        'ya_calificado': ya_calificado,  # Enviamos esta variable
    })




def detalle_serie(request, id):
    serie = get_object_or_404(Serie, id=id)

    # Calcular el promedio de calificaciones
    promedio_calificacion = UsuarioContenido.objects.filter(
        serie=serie,
        calificacion__isnull=False
    ).aggregate(promedio=Avg('calificacion'))['promedio']

    tu_calificacion = None
    es_favorito = False
    es_visto = False
    ya_calificado = False  # Nuevo

    if request.user.is_authenticated:
        usuario_contenido = UsuarioContenido.objects.filter(
            usuario=request.user,
            serie=serie
        ).first()

        if usuario_contenido:
            tu_calificacion = usuario_contenido.calificacion
            es_favorito = usuario_contenido.favorito
            es_visto = usuario_contenido.visto
            ya_calificado = usuario_contenido.calificacion is not None  # Verificar si ya calificó

    return render(request, 'ClonFlixApp/detalle_serie.html', {
        'serie': serie,
        'promedio_calificacion': round(promedio_calificacion, 1) if promedio_calificacion else None,
        'tu_calificacion': tu_calificacion,
        'es_favorito': es_favorito,
        'es_visto': es_visto,
        'ya_calificado': ya_calificado,  # Enviamos esta variable
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
    """
    Vista para manejar la calificación de contenido (películas o series).
    """
    # Determinar el modelo según el tipo de contenido
    modelo = Pelicula if tipo == 'pelicula' else Serie
    contenido = get_object_or_404(modelo, id=contenido_id)

    if request.method == 'POST':
        # Obtener la calificación enviada por el usuario
        calificacion = request.POST.get('calificacion')

        # Validar que la calificación sea un número entre 1 y 10
        if not calificacion or not calificacion.isdigit() or not (1 <= int(calificacion) <= 10):
            messages.error(request, 'Calificación inválida. Debe ser un número entre 1 y 10.')
            return redirect(request.META.get('HTTP_REFERER', '/'))

        calificacion = int(calificacion)

        # Obtener o crear el registro en UsuarioContenido
        usuario_contenido, created = UsuarioContenido.objects.get_or_create(
            usuario=request.user,
            pelicula=contenido if tipo == 'pelicula' else None,
            serie=contenido if tipo == 'serie' else None,
        )

        # Actualizar la calificación
        usuario_contenido.calificacion = calificacion
        usuario_contenido.save()

        # Mensaje de confirmación
        messages.success(request, f'Has calificado {contenido.titulo} con un {calificacion}/10.')

        # Redirigir a la página previa
        return redirect(request.META.get('HTTP_REFERER', '/'))

    # Si no es un método POST, redirigir a la página de detalle
    return redirect('ClonFlixApp:detalle_pelicula' if tipo == 'pelicula' else 'ClonFlixApp:detalle_serie', id=contenido_id)
