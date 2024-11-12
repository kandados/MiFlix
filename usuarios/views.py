from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Usuario, UsuarioContenido
from contenido.models import Contenido

def inicio(request):
    return render(request, 'clonflixapp/index.html')  # Página principal

# Decorador para verificar si el usuario es administrador
def es_administrador(user):
    return user.is_authenticated and user.es_administrador

# Vista de registro
def registro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # Validación de email
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "El correo electrónico no es válido.")
            return redirect('registro')

        # Validación de contraseña
        if len(password) < 8:
            messages.error(request, "La contraseña debe tener al menos 8 caracteres.")
            return redirect('registro')

        # Verificar si el usuario ya existe
        if Usuario.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
            return redirect('registro')
        else:
            # Crear el usuario y guardar en la base de datos
            user = Usuario.objects.create_user(username=username, password=password, email=email)
            messages.success(request, f'Registro exitoso. ¡Bienvenido, {user.username}!')

            # Autenticar e iniciar sesión automáticamente
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirigir a la página principal de inicio

    return render(request, 'usuarios/registro.html')

# Vista de login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido, {user.username}!')
            return redirect('index')  # Redirigir a la página principal
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'usuarios/login.html')

# Otras vistas...


@login_required
def panel_admin(request):
    return render(request, 'usuarios/panel-admin.html')

@login_required
def panel_usuario(request):
    return render(request, 'usuarios/panel_usuario.html')

# Vistas para gestión de usuarios (solo para administradores)
@login_required
@user_passes_test(es_administrador)
def gestion_usuarios(request):
    clientes = Usuario.objects.filter(es_cliente=True)
    return render(request, 'usuarios/gestion_usuarios.html', {'clientes': clientes})

@login_required
@user_passes_test(es_administrador)
def editar_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id, es_cliente=True)
    if request.method == 'POST':
        usuario.es_cliente = request.POST.get('es_cliente', usuario.es_cliente)
        usuario.save()
        return redirect('gestion_usuarios')
    return render(request, 'usuarios/editar_usuario.html', {'usuario': usuario})

@login_required
@user_passes_test(es_administrador)
def eliminar_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id, es_cliente=True)
    if request.method == 'POST':
        usuario.delete()
        return redirect('gestion_usuarios')
    return render(request, 'usuarios/eliminar_usuario.html', {'usuario': usuario})

# Vistas para gestión de contenido (solo para administradores)
@login_required
@user_passes_test(es_administrador)
def gestion_contenido(request):
    contenido = Contenido.objects.all()
    return render(request, 'usuarios/gestion_contenido.html', {'contenido': contenido})

@login_required
@user_passes_test(es_administrador)
def crear_contenido(request):
    if request.method == 'POST':
        titulo = request.POST['titulo']
        sinopsis = request.POST['sinopsis']
        tipo = request.POST['tipo']
        fecha_publicacion = request.POST['fecha_publicacion']
        nuevo_contenido = Contenido(
            titulo=titulo,
            sinopsis=sinopsis,
            tipo=tipo,
            fecha_publicacion=fecha_publicacion
        )
        nuevo_contenido.save()
        return redirect('gestion_contenido')
    return render(request, 'usuarios/crear_contenido.html')

@login_required
@user_passes_test(es_administrador)
def editar_contenido(request, contenido_id):
    contenido = get_object_or_404(Contenido, id=contenido_id)
    if request.method == 'POST':
        contenido.titulo = request.POST['titulo']
        contenido.sinopsis = request.POST['sinopsis']
        contenido.tipo = request.POST['tipo']
        contenido.fecha_publicacion = request.POST['fecha_publicacion']
        contenido.save()
        return redirect('gestion_contenido')
    return render(request, 'usuarios/editar_contenido.html', {'contenido': contenido})

@login_required
@user_passes_test(es_administrador)
def eliminar_contenido(request, contenido_id):
    contenido = get_object_or_404(Contenido, id=contenido_id)
    if request.method == 'POST':
        contenido.delete()
        return redirect('gestion_contenido')
    return render(request, 'usuarios/eliminar_contenido.html', {'contenido': contenido})

@login_required
@user_passes_test(es_administrador)
def ver_estadisticas(request):
    total_usuarios = Usuario.objects.count()
    total_contenido = Contenido.objects.count()
    return render(request, 'usuarios/ver_estadisticas.html', {'total_usuarios': total_usuarios, 'total_contenido': total_contenido})

# Vistas adicionales para el panel de usuario
@login_required
def favoritos(request):
    return render(request, 'usuarios/favoritos.html')

@login_required
def historial(request):
    return render(request, 'usuarios/historial.html')

@login_required
def explorar(request):
    return render(request, 'usuarios/explorar.html')

@login_required
def inicio_personalizado(request):
    # Obtenemos todas las secciones de contenido
    generos = Contenido.objects.values_list('tipo', flat=True).distinct()
    peliculas_recientes = Contenido.objects.filter(tipo='pelicula').order_by('-fecha_publicacion')[:10]
    series_recientes = Contenido.objects.filter(tipo='serie').order_by('-fecha_publicacion')[:10]

    # Obtenemos el estado de interacción del usuario con cada contenido
    usuario_contenido = UsuarioContenido.objects.filter(usuario=request.user)
    favoritos_ids = usuario_contenido.filter(favorito=True).values_list('contenido_id', flat=True)
    visto_ids = usuario_contenido.filter(visto=True).values_list('contenido_id', flat=True)
    ver_mas_tarde_ids = usuario_contenido.filter(ver_mas_tarde=True).values_list('contenido_id', flat=True)

    return render(request, 'usuarios/inicio_personalizado.html', {
        'generos': generos,
        'peliculas_recientes': peliculas_recientes,
        'series_recientes': series_recientes,
        'favoritos_ids': favoritos_ids,
        'visto_ids': visto_ids,
        'ver_mas_tarde_ids': ver_mas_tarde_ids,
    })


@login_required
def marcar_favorito(request, contenido_id):
    contenido = get_object_or_404(Contenido, id=contenido_id)
    usuario_contenido, created = UsuarioContenido.objects.get_or_create(usuario=request.user, contenido=contenido)
    usuario_contenido.favorito = not usuario_contenido.favorito
    usuario_contenido.save()
    return redirect('inicio_personalizado')

@login_required
def marcar_visto(request, contenido_id):
    contenido = get_object_or_404(Contenido, id=contenido_id)
    usuario_contenido, created = UsuarioContenido.objects.get_or_create(usuario=request.user, contenido=contenido)
    usuario_contenido.visto = not usuario_contenido.visto
    usuario_contenido.save()
    return redirect('inicio_personalizado')

@login_required
def marcar_ver_mas_tarde(request, contenido_id):
    contenido = get_object_or_404(Contenido, id=contenido_id)
    usuario_contenido, created = UsuarioContenido.objects.get_or_create(usuario=request.user, contenido=contenido)
    usuario_contenido.ver_mas_tarde = True  # Marca el contenido para ver más tarde
    usuario_contenido.save()
    return redirect('detalle_pelicula', id=contenido_id) if contenido.tipo == 'pelicula' else redirect('detalle_serie', id=contenido_id)

@login_required
def puntuar_contenido(request, contenido_id):
    # Implementa la lógica de puntuación aquí, por ejemplo, usando una calificación de 1 a 5
    pass
