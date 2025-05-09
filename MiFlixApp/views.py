from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Q
from unidecode import unidecode
from usuarios.models import UsuarioPelicula, UsuarioContenido, UsuarioSerie
from MiFlixApp.models import Pelicula, Serie



# Para el video de la pagina de inicio
def video_page(request):
    # Ruta del archivo de video
    video_url = '/media/movie_videos/sample_movie.mp4'
    return render(request, 'video.html', {'video_url': video_url})



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
    return render(request, 'MiFlixApp/index.html', context)


# Novedades más vistas
def novedades_mas_vistas(request):
    # Películas más vistas
    novedades_peliculas = Pelicula.objects.order_by('-vistas_totales', '-calificacion_usuario', 'titulo')[:12]

    # Series más vistas
    novedades_series = Serie.objects.order_by('-vistas_totales', '-calificacion_usuario', 'titulo')[:12]

    return render(request, 'MiFlixApp/novedades_mas_vistas.html', {
        'novedades_peliculas': novedades_peliculas,
        'novedades_series': novedades_series,
    })



# Películas por género
def peliculas_por_genero(request, genre):
    peliculas = Pelicula.objects.filter(genero__iexact=genre)
    return render(request, 'MiFlixApp/peliculas_por_genero.html', {
        'peliculas': peliculas,
        'genero': genre.capitalize(),
    })


# Series recientes
def series_recientes(request):
    series = Serie.objects.all().order_by('-estreno')[:10]
    return render(request, 'MiFlixApp/series_recientes.html', {'series': series})


# Búsqueda de contenido

def buscar_contenido(request):
    query = request.GET.get('q', '').strip()  # Obtiene la consulta
    peliculas = Pelicula.objects.none()
    series = Serie.objects.none()

    if query:
        # Normaliza la consulta (sin tildes y en minúsculas)
        normalized_query = unidecode(query).lower()

        # Buscar por ID con el prefijo 'id'
        if normalized_query.startswith('id') and normalized_query[2:].isdigit():
            # Extraer el número después de 'id'
            id_number = normalized_query[2:]
            peliculas = Pelicula.objects.filter(
                Q(id=id_number)
            ).distinct()
            series = Serie.objects.filter(
                Q(id=id_number)
            ).distinct()

        # Buscar por año exacto (4 cifras)
        elif normalized_query.isdigit() and len(normalized_query) == 4:
            peliculas = Pelicula.objects.filter(
                Q(estreno=int(normalized_query))
            ).distinct()
            series = Serie.objects.filter(
                Q(estreno=int(normalized_query))
            ).distinct()

        # Búsqueda general para texto
        else:
            peliculas = Pelicula.objects.filter(
                Q(titulo__icontains=normalized_query) |
                Q(genero__icontains=normalized_query) |
                Q(director__icontains=normalized_query) |
                Q(protagonistas__icontains=normalized_query)
            ).distinct()
            series = Serie.objects.filter(
                Q(titulo__icontains=normalized_query) |
                Q(genero__icontains=normalized_query) |
                Q(director__icontains=normalized_query) |
                Q(protagonistas__icontains=normalized_query)
            ).distinct()

    # Si no hay resultados
    sin_resultados = not (peliculas.exists() or series.exists())

    return render(request, 'MiFlixApp/buscar_resultados.html', {
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

    return render(request, 'MiFlixApp/detalle_pelicula.html', {
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
            ya_calificado = usuario_contenido.calificacion is not None  # Verificar si ya se calificó

    return render(request, 'MiFlixApp/detalle_serie.html', {
        'serie': serie,
        'promedio_calificacion': round(promedio_calificacion, 1) if promedio_calificacion else None,
        'tu_calificacion': tu_calificacion,
        'es_favorito': es_favorito,
        'es_visto': es_visto,
        'ya_calificado': ya_calificado,
        # Enviamos esta variable
    })
# Vistas para series y películas
def series_view(request):
    series = Serie.objects.all()
    return render(request, 'MiFlixApp/series.html', {'series': series})


def peliculas_view(request):
    peliculas = Pelicula.objects.all()
    return render(request, 'MiFlixApp/peliculas.html', {'peliculas': peliculas})


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

        # Recalcular la calificación promedio
        if tipo == 'pelicula':
            promedio = UsuarioContenido.objects.filter(pelicula=contenido).aggregate(Avg('calificacion'))['calificacion__avg']
            contenido.calificacion_usuario = promedio or 0  # Actualizar el campo en Pelicula
        else:
            promedio = UsuarioContenido.objects.filter(serie=contenido).aggregate(Avg('calificacion'))['calificacion__avg']
            contenido.calificacion_usuario = promedio or 0  # Actualizar el campo en Serie

        contenido.save()  # Guardar el promedio calculado en el modelo principal

        # Mensaje de confirmación
        messages.success(request, f'Has calificado {contenido.titulo} con un {calificacion}/10.')

        # Redirigir a la página previa
        return redirect(request.META.get('HTTP_REFERER', '/'))

  #Si no es un método POST, redirigir a la página de detalle
    return redirect('MiFlixApp:detalle_pelicula' if tipo == 'pelicula' else 'MiFlixApp:detalle_serie', id=contenido_id)