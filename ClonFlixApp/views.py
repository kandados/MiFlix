from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from usuarios.models import UsuarioContenido
from contenido.models import Contenido

# Diccionario para traducir géneros al español
GENRE_TRANSLATIONS = {
    'accion': 'Acción',
    'comedia': 'Comedia',
    'drama': 'Drama',
    'terror': 'Terror',
    'romance': 'Romance',
    'ciencia_ficcion': 'Ciencia Ficción',
    'fantasia': 'Fantasía',
}

# Página principal
def index(request):
    # Selecciona las 4 películas con la mayor calificación de usuario como "destacadas"
    peliculas_destacadas = Contenido.objects.filter(tipo='pelicula').order_by('-calificacion_usuario')[:4]
    peliculas_recientes = Contenido.objects.filter(tipo='pelicula').order_by('-estreno')[:4]
    series_recientes = Contenido.objects.filter(tipo='serie').order_by('-estreno')[:4]

    if request.user.is_authenticated:
        usuario_contenido = UsuarioContenido.objects.filter(usuario=request.user)
        favoritos_ids = usuario_contenido.filter(favorito=True).values_list('contenido_id', flat=True)
        visto_ids = usuario_contenido.filter(visto=True).values_list('contenido_id', flat=True)
        ver_mas_tarde_ids = usuario_contenido.filter(ver_mas_tarde=True).values_list('contenido_id', flat=True)
    else:
        favoritos_ids = []
        visto_ids = []
        ver_mas_tarde_ids = []

    return render(request, 'ClonFlixApp/index.html', {
        'peliculas_destacadas': peliculas_destacadas,
        'peliculas_recientes': peliculas_recientes,
        'series_recientes': series_recientes,
        'favoritos_ids': favoritos_ids,
        'visto_ids': visto_ids,
        'ver_mas_tarde_ids': ver_mas_tarde_ids,
    })

# Vistas para series y películas con botones de interacción
def series_view(request):
    series = Contenido.objects.filter(tipo='serie')
    favoritos_ids = []
    visto_ids = []
    ver_mas_tarde_ids = []

    if request.user.is_authenticated:
        usuario_contenido = UsuarioContenido.objects.filter(usuario=request.user)
        favoritos_ids = usuario_contenido.filter(favorito=True).values_list('contenido_id', flat=True)
        visto_ids = usuario_contenido.filter(visto=True).values_list('contenido_id', flat=True)
        ver_mas_tarde_ids = usuario_contenido.filter(ver_mas_tarde=True).values_list('contenido_id', flat=True)

    return render(request, 'ClonFlixApp/series.html', {
        'series': series,
        'favoritos_ids': favoritos_ids,
        'visto_ids': visto_ids,
        'ver_mas_tarde_ids': ver_mas_tarde_ids,
    })

def peliculas_view(request):
    peliculas = Contenido.objects.filter(tipo='pelicula')
    favoritos_ids = []
    visto_ids = []
    ver_mas_tarde_ids = []

    if request.user.is_authenticated:
        usuario_contenido = UsuarioContenido.objects.filter(usuario=request.user)
        favoritos_ids = usuario_contenido.filter(favorito=True).values_list('contenido_id', flat=True)
        visto_ids = usuario_contenido.filter(visto=True).values_list('contenido_id', flat=True)
        ver_mas_tarde_ids = usuario_contenido.filter(ver_mas_tarde=True).values_list('contenido_id', flat=True)

    return render(request, 'ClonFlixApp/peliculas.html', {
        'peliculas': peliculas,
        'favoritos_ids': favoritos_ids,
        'visto_ids': visto_ids,
        'ver_mas_tarde_ids': ver_mas_tarde_ids,
    })

def peliculas_por_genero(request, genre):
    peliculas = Contenido.objects.filter(genero=genre)
    genre_spanish = GENRE_TRANSLATIONS.get(genre, genre).capitalize()
    return render(request, 'ClonFlixApp/peliculas_por_genero.html', {
        'peliculas': peliculas,
        'genre': f'Películas de {genre_spanish}',
    })

def lista_peliculas(request):
    peliculas = Contenido.objects.all()
    return render(request, 'ClonFlixApp/lista_peliculas.html', {'peliculas': peliculas})

def detalle_pelicula(request, id):
    contenido = get_object_or_404(Contenido, id=id)
    return render(request, 'ClonFlixApp/detalle_pelicula.html', {'contenido': contenido})

def buscar_peliculas(request):
    query = request.GET.get('q')
    peliculas = Contenido.objects.filter(titulo__icontains=query)
    return render(request, 'ClonFlixApp/buscar_peliculas.html', {
        'peliculas': peliculas,
        'query': query,
    })

def novedades_mas_vistas(request):
    novedades = Contenido.objects.order_by('-calificacion_usuario')[:8]
    return render(request, 'ClonFlixApp/novedades_mas_vistas.html', {'novedades': novedades})

def recomendacion_usuarios(request):
    recomendaciones = Contenido.objects.all().order_by('?')[:10]
    return render(request, 'ClonFlixApp/recomendacion_usuarios.html', {'recomendaciones': recomendaciones})

def series_recientes(request):
    series = Contenido.objects.filter(tipo='serie').order_by('-estreno')[:10]
    return render(request, 'ClonFlixApp/series_recientes.html', {'series': series})

def detalle_serie(request, id):
    serie = get_object_or_404(Contenido, id=id, tipo='serie')
    return render(request, 'ClonFlixApp/detalle_serie.html', {'serie': serie})

# Acciones con el usuario Logueado
@login_required
def mi_lista_view(request):
    mi_lista = Contenido.objects.filter(usuariocontenido__usuario=request.user, usuariocontenido__favorito=True)
    usuario_contenido = UsuarioContenido.objects.filter(usuario=request.user)
    favoritos_ids = usuario_contenido.filter(favorito=True).values_list('contenido_id', flat=True)
    visto_ids = usuario_contenido.filter(visto=True).values_list('contenido_id', flat=True)
    ver_mas_tarde_ids = usuario_contenido.filter(ver_mas_tarde=True).values_list('contenido_id', flat=True)

    return render(request, 'ClonFlixApp/mi_lista.html', {
        'mi_lista': mi_lista,
        'favoritos_ids': favoritos_ids,
        'visto_ids': visto_ids,
        'ver_mas_tarde_ids': ver_mas_tarde_ids,
    })

@login_required
def marcar_favorito(request, id):
    pelicula = get_object_or_404(Contenido, id=id)
    usuario_contenido, created = UsuarioContenido.objects.get_or_create(usuario=request.user, contenido=pelicula)
    usuario_contenido.favorito = not usuario_contenido.favorito
    usuario_contenido.save()
    return redirect('detalle_pelicula', id=id)

@login_required
def marcar_visto(request, id):
    pelicula = get_object_or_404(Contenido, id=id)
    usuario_contenido, created = UsuarioContenido.objects.get_or_create(usuario=request.user, contenido=pelicula)
    usuario_contenido.visto = not usuario_contenido.visto
    usuario_contenido.save()
    return redirect('detalle_pelicula', id=id)

@login_required
def marcar_ver_mas_tarde(request, id):
    pelicula = get_object_or_404(Contenido, id=id)
    usuario_contenido, created = UsuarioContenido.objects.get_or_create(usuario=request.user, contenido=pelicula)
    usuario_contenido.ver_mas_tarde = not usuario_contenido.ver_mas_tarde
    usuario_contenido.save()
    return redirect('detalle_pelicula', id=id)
