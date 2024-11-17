from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Usuario, UsuarioContenido
from ClonFlixApp.models import Pelicula, Serie

def inicio(request):
    return render(request, 'usuarios/inicio.html')

def registro(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        if Usuario.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
            return redirect('usuarios:registro')
        try:
            user = Usuario.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            messages.success(request, 'Registro exitoso.')
            return redirect('usuarios:index')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    return render(request, 'usuarios/registro.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('usuarios:index')
        messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'usuarios/login.html')

@login_required
def panel_usuario(request):
    return render(request, 'usuarios/panel_usuario.html')

@login_required
def panel_admin(request):
    return render(request, 'usuarios/panel_admin.html')

# Función para verificar si el usuario es administrador
def es_administrador(user):
    return user.is_authenticated and user.role == 'ADMIN'

@login_required
@user_passes_test(es_administrador)
def gestion_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/gestion_usuarios.html', {'usuarios': usuarios})

@login_required
@user_passes_test(es_administrador)
def editar_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    if request.method == 'POST':
        usuario.username = request.POST.get('username', usuario.username)
        usuario.email = request.POST.get('email', usuario.email)
        usuario.save()
        return redirect('usuarios:gestion_usuarios')
    return render(request, 'usuarios/editar_usuario.html', {'usuario': usuario})

@login_required
@user_passes_test(es_administrador)
def eliminar_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    if request.method == 'POST':  # Confirmación antes de eliminar
        usuario.delete()
        return redirect('usuarios:gestion_usuarios')  # Redirigir a la página de gestión de usuarios
    return render(request, 'usuarios/eliminar_usuario.html', {'usuario': usuario})



@login_required
def favoritos(request):
    favoritos = UsuarioContenido.objects.filter(usuario=request.user, pelicula__isnull=False)
    return render(request, 'usuarios/favoritos.html', {'favoritos': favoritos})

@login_required
def agregar_a_mi_lista(request, contenido_id, tipo):
    if tipo == 'pelicula':
        contenido = get_object_or_404(Pelicula, id=contenido_id)
    elif tipo == 'serie':
        contenido = get_object_or_404(Serie, id=contenido_id)
    else:
        messages.error(request, 'Tipo de contenido no válido.')
        return redirect('usuarios:index')
    UsuarioContenido.objects.get_or_create(usuario=request.user, pelicula=contenido if tipo == 'pelicula' else None,
                                           serie=contenido if tipo == 'serie' else None)
    messages.success(request, f'{contenido.titulo} ha sido añadido a tu lista.')
    return redirect('usuarios:index')


@login_required
def marcar_favorito(request, contenido_id, tipo):
    # Obtener el contenido basado en el ID y el tipo
    contenido = get_object_or_404(Contenido, id=contenido_id, tipo=tipo)

    # Verificar si el contenido ya está en favoritos
    usuario_contenido, created = UsuarioContenido.objects.get_or_create(
        usuario=request.user,
        contenido=contenido
    )
    # Alternar el estado de favorito
    usuario_contenido.favorito = not usuario_contenido.favorito
    usuario_contenido.save()

    # Redirigir a la página anterior
    return redirect(request.META.get('HTTP_REFERER', 'usuarios:index'))