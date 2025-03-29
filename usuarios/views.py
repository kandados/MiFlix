from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Usuario, UsuarioContenido
from MiFlixApp.models import Pelicula, Serie
from django.db.models import Count
from django.db.models import Q
from MiFlixApp.forms import PeliculaForm
from MiFlixApp.forms import SerieForm
import plotly.graph_objects as go
from django.shortcuts import render
from django.db.models import Sum
from usuarios.models import UsuarioSerie, UsuarioPelicula


# ============================
# Panel usuario
# ============================
@login_required
def panel_usuario(request):
    return render(request, 'usuarios/panel_usuario.html')

def inicio_personalizado(request):
    return render(request, 'MiFlixApp:index.html')

# ======================================================== #
# Registro de un usuario y Login de un usuario 'No Admin'  #
# ======================================================== #

def registro(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        # Verificar si el nombre de usuario ya existe
        if Usuario.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe, utiliza otro nombre.')
            return redirect('usuarios:registro')

        # Verificar si el email ya está registrado
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'El email ya existe, utiliza otro diferente.')
            return redirect('usuarios:registro')

        try:
            user = Usuario.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            messages.success(request, 'Registrado con éxito.')
            return redirect('usuarios:panel_usuario')  # Redirige al panel de usuario
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('usuarios:registro')

    return render(request, 'usuarios/registro.html')


# login Inicio de sesión como usuario o como Admin
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Si el usuario es un administrador, redirigir al panel admin
            if user.is_staff or user.is_superuser:
                return redirect('usuarios:panel_admin')  # Redirigir al panel de administración

            # Redirigir a la página de inicio para cualquier usuario no administrador
            return redirect('MiFlixApp:index')  # Redirigir al inicio como usuario registrado

        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'usuarios/login.html')



# Función para verificar si un usuario es administrador
def es_administrador(user):
    return user.is_authenticated and user.is_staff


# ============================
# Autenticación y Sesión Admin
# ============================
@login_required
def panel_admin(request):
    return render(request, 'usuarios/panel_admin.html')

# ============================
# Gestión de Usuarios Admin
# ============================

@login_required
@user_passes_test(es_administrador)
def gestion_usuarios(request):
    query = request.GET.get('q', '').strip()  # Captura y limpia el término de búsqueda
    usuarios = Usuario.objects.all()  # Consulta base inicial

    if query:
        # Construimos el filtro dinámicamente
        filtro = Q()

        # Filtro por ID (si la búsqueda es numérica)
        if query.isdigit():
            filtro |= Q(id=query)

        # Filtro por nombre de usuario
        filtro |= Q(username__icontains=query)

        # Filtro por correo electrónico
        filtro |= Q(email__icontains=query)

        # Filtro por rol
        if query.lower() in ['admin', 'administrador']:
            filtro |= Q(is_staff=True)
        elif query.lower() == 'usuario':
            filtro |= Q(is_staff=False)

        # Aplicamos el filtro a la consulta
        usuarios = usuarios.filter(filtro)

    return render(request, 'usuarios/gestion_usuarios.html', {'usuarios': usuarios})



@login_required
@user_passes_test(es_administrador)
def crear_usuario(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        Usuario.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Usuario creado correctamente.")
        return redirect('usuarios:gestion_usuarios')
    return render(request, 'usuarios/crear_usuario.html')

@login_required
@user_passes_test(es_administrador)
def editar_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    if request.method == 'POST':
        usuario.username = request.POST['username']
        usuario.email = request.POST['email']
        if request.POST['password']:
            usuario.set_password(request.POST['password'])
        usuario.save()
        messages.success(request, "Usuario actualizado correctamente.")
        return redirect('usuarios:gestion_usuarios')
    return render(request, 'usuarios/editar_usuario.html', {'usuario': usuario})

@login_required
@user_passes_test(es_administrador)
def eliminar_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    if request.method == 'POST':  # Confirmar eliminación
        usuario.delete()
        messages.success(request, f'El usuario "{usuario.username}" ha sido eliminado correctamente.')
        return redirect('usuarios:gestion_usuarios')  # Redirigir a la lista de usuarios
    return render(request, 'usuarios/eliminar_usuario.html', {'usuario': usuario})

# ============================
# Gestión de Contenidos Admin
# ============================
@login_required
@user_passes_test(es_administrador)
def gestion_contenidos(request):
    # Capturar el término de búsqueda
    query = request.GET.get('q', '').strip()

    # Obtener todas las películas y series
    peliculas = Pelicula.objects.all()
    series = Serie.objects.all()

    # Filtrar si hay un término de búsqueda
    if query:
        peliculas = peliculas.filter(titulo__icontains=query)  # Filtrar por título de película
        series = series.filter(titulo__icontains=query)        # Filtrar por título de serie

    return render(request, 'usuarios/gestion_contenidos.html', {
        'peliculas': peliculas,
        'series': series,
        'query': query,  # Pasar el término de búsqueda para que se muestre en el campo de texto
    })

@login_required
@user_passes_test(es_administrador)
def crear_pelicula(request):
    if request.method == 'POST':
        form = PeliculaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('MiFlixApp:peliculas')
    else:
        form = PeliculaForm()
    return render(request, 'usuarios/crear_pelicula.html', {'form': form})

@login_required
@user_passes_test(es_administrador)
def crear_serie(request):
    if request.method == 'POST':
        form = SerieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('usuarios:gestion_contenidos')  # Ajusta esta redirección según tu proyecto
    else:
        form = SerieForm()
    return render(request, 'usuarios/crear_serie.html', {'form': form})

@login_required
@user_passes_test(es_administrador)
def editar_pelicula(request, pelicula_id):
    # Obtener la película a editar
    pelicula = get_object_or_404(Pelicula, id=pelicula_id)

    if request.method == 'POST':
        # Cargar el formulario con los datos enviados
        form = PeliculaForm(request.POST, request.FILES, instance=pelicula)
        if form.is_valid():
            form.save()
            return redirect('usuarios:gestion_contenidos')  # Redirige a la gestion de contenidos
    else:
        # Cargar el formulario con los datos de la película
        form = PeliculaForm(instance=pelicula)

    return render(request, 'usuarios/editar_pelicula.html', {'form': form, 'pelicula': pelicula})


@login_required
@user_passes_test(es_administrador)
def eliminar_pelicula(request, pelicula_id):
    pelicula = get_object_or_404(Pelicula, id=pelicula_id)
    if request.method == 'POST':  # Confirmar eliminación
        pelicula.delete()
        messages.success(request, f'La película "{pelicula.titulo}" ha sido eliminada correctamente.')
        return redirect('usuarios:gestion_contenidos')  # Redirigir a la gestión de contenidos
    return render(request, 'usuarios/eliminar_pelicula.html', {'pelicula': pelicula})



@login_required
@user_passes_test(es_administrador)
def editar_serie(request, serie_id):
    # Obtener la serie a editar
    serie = get_object_or_404(Serie, id=serie_id)

    if request.method == 'POST':
        # Cargar el formulario con los datos enviados
        form = SerieForm(request.POST, request.FILES, instance=serie)
        if form.is_valid():
            form.save()
            messages.success(request, 'Serie actualizada exitosamente.')
            return redirect('usuarios:gestion_contenidos')
    else:
        # Cargar el formulario con los datos actuales de la serie
        form = SerieForm(instance=serie)

    return render(request, 'usuarios/editar_serie.html', {'form': form, 'serie': serie})

@login_required
@user_passes_test(es_administrador)
def eliminar_serie(request, serie_id):
    serie = get_object_or_404(Serie, id=serie_id)
    if request.method == 'POST':
        serie.delete()
        messages.success(request, 'Serie eliminada exitosamente.')
        return redirect('usuarios:gestion_contenidos')
    return render(request, 'usuarios/eliminar_serie.html', {'serie': serie})



# =============================================================== #
# Favoritos, calificar, Ya Vistas y estadisticas Usuario Logueado #
# =============================================================== #
@login_required
def favoritas_view(request):
    favoritos_peliculas = UsuarioContenido.objects.filter(usuario=request.user, favorito=True, pelicula__isnull=False)
    favoritos_series = UsuarioContenido.objects.filter(usuario=request.user, favorito=True, serie__isnull=False)
    return render(request, 'usuarios/favoritas.html', {
        'favoritos_peliculas': favoritos_peliculas,
        'favoritos_series': favoritos_series,
    })

@login_required
def ya_vistas_view(request):
    vistas_peliculas = UsuarioContenido.objects.filter(usuario=request.user, visto=True, pelicula__isnull=False)
    vistas_series = UsuarioContenido.objects.filter(usuario=request.user, visto=True, serie__isnull=False)
    return render(request, 'usuarios/ya_vistas.html', {
        'vistas_peliculas': vistas_peliculas,
        'vistas_series': vistas_series,
    })

@login_required
def marcar_favorito(request, contenido_id, tipo):
    # Determinar si es película o serie
    modelo = Pelicula if tipo == 'pelicula' else Serie
    contenido = get_object_or_404(modelo, id=contenido_id)

    # Obtener o crear un registro en UsuarioContenido
    usuario_contenido, created = UsuarioContenido.objects.get_or_create(
        usuario=request.user,
        pelicula=contenido if tipo == 'pelicula' else None,
        serie=contenido if tipo == 'serie' else None,
    )

    # Cambiar solo el estado de "favorito"
    usuario_contenido.favorito = not usuario_contenido.favorito
    usuario_contenido.save()

    # Mensaje de confirmación
    messages.success(request, f'{contenido.titulo} {"añadido a" if usuario_contenido.favorito else "eliminado de"} tus favoritos.')

    # Redirigir a la página previa
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def marcar_como_visto(request, contenido_id, tipo):
    # Verifica si el tipo es película o serie
    if tipo not in ['pelicula', 'serie']:
        messages.error(request, 'Tipo de contenido no válido.')
        return redirect('usuarios:ya_vistas')

    # obtenemos el contenido según el tipo
    modelo = Pelicula if tipo == 'pelicula' else Serie
    contenido = get_object_or_404(modelo, id=contenido_id)

    # Creamos o actualizamos el registro en UsuarioContenido
    usuario_contenido, created = UsuarioContenido.objects.get_or_create(
        usuario=request.user,
        pelicula=contenido if tipo == 'pelicula' else None,
        serie=contenido if tipo == 'serie' else None,
    )

    # Alternar el estado de "visto"
    if not usuario_contenido.visto:  # Si aún no está marcado como visto
        usuario_contenido.visto = True
        contenido.vistas_totales += 1  # Incrementar vistas totales
        contenido.save()  # Guardar en el modelo
        messages.success(request, f'{contenido.titulo} ha sido marcado como visto.')
    else:  # Si ya estaba marcado como visto
        usuario_contenido.visto = False
        contenido.vistas_totales = max(contenido.vistas_totales - 1, 0)  # Restar vistas sin ir por debajo de 0
        contenido.save()
        messages.success(request, f'{contenido.titulo} ha sido desmarcado como visto.')

    usuario_contenido.save()

    # Redirigir a la página previa o a ya vistas
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def estadisticas_usuario(request):
    usuario = request.user

    # Métricas individuales
    peliculas_vistas = usuario.mi_lista.filter(pelicula__isnull=False, visto=True).count()
    series_vistas = usuario.mi_lista.filter(serie__isnull=False, visto=True).count()

    # Tiempo dedicado (Películas y Series)
    tiempo_peliculas = usuario.mi_lista.filter(pelicula__isnull=False, visto=True).aggregate(total=Sum('pelicula__duracion'))['total'] or 0
    tiempo_series = usuario.mi_lista.filter(serie__isnull=False, visto=True).aggregate(total=Sum('serie__duracion_media_capitulo'))['total'] or 0

    # Distribución de géneros (Películas)
    peliculas_generos = usuario.mi_lista.filter(pelicula__isnull=False, visto=True).values('pelicula__genero').annotate(total=Count('pelicula__genero'))
    series_generos = usuario.mi_lista.filter(serie__isnull=False, visto=True).values('serie__genero').annotate(total=Count('serie__genero'))

    # Estilo general de las gráficas
    layout_estilo = go.Layout(
        paper_bgcolor='rgba(31, 41, 55, 1)',  # Fondo general
        plot_bgcolor='rgba(31, 41, 55, 1)',   # Fondo del área de la gráfica
        font=dict(color="white"),            # Texto blanco
        title_font=dict(size=16, color="white"),  # Títulos más pequeños
        height=300,  # Altura compacta
        width=400,   # Ancho compacto
    )

    # Gráfica 1: Tiempo en Películas
    fig_peliculas_tiempo = go.Figure(go.Indicator(
        mode="gauge+number",
        value=tiempo_peliculas,
        title={'text': "Minutos en Películas"},
        gauge={
            'axis': {'range': [None, max(tiempo_peliculas * 1.2, 1000)]},
            'bar': {'color': "green"},
        }
    ))
    fig_peliculas_tiempo.update_layout(layout_estilo)

    # Gráfica 2: Tiempo en Series
    fig_series_tiempo = go.Figure(go.Indicator(
        mode="gauge+number",
        value=tiempo_series,
        title={'text': "Minutos en Series"},
        gauge={
            'axis': {'range': [None, max(tiempo_series * 1.2, 1000)]},
            'bar': {'color': "blue"},
        }
    ))
    fig_series_tiempo.update_layout(layout_estilo)

    # Gráfica 3: Distribución de Géneros (Películas)
    fig_peliculas_generos = go.Figure(data=[go.Pie(
        labels=[item['pelicula__genero'] for item in peliculas_generos],
        values=[item['total'] for item in peliculas_generos],
        hole=.4  # Gráfica tipo "donut"
    )])
    fig_peliculas_generos.update_layout(layout_estilo, title="Distribución de Géneros en Películas")

    # Gráfica 4: Distribución de Géneros (Series)
    fig_series_generos = go.Figure(data=[go.Pie(
        labels=[item['serie__genero'] for item in series_generos],
        values=[item['total'] for item in series_generos],
        hole=.4  # Gráfica tipo "donut"
    )])
    fig_series_generos.update_layout(layout_estilo, title="Distribución de Géneros en Series")

    # Convertir gráficos a html
    chart_peliculas_tiempo = fig_peliculas_tiempo.to_html(full_html=False)
    chart_series_tiempo = fig_series_tiempo.to_html(full_html=False)
    chart_peliculas_generos = fig_peliculas_generos.to_html(full_html=False)
    chart_series_generos = fig_series_generos.to_html(full_html=False)

    return render(request, 'usuarios/estadisticas_usuario.html', {
        'usuario': usuario,
        'peliculas_vistas': peliculas_vistas,
        'series_vistas': series_vistas,
        'tiempo_peliculas': tiempo_peliculas,
        'tiempo_series': tiempo_series,
        'chart_peliculas_tiempo': chart_peliculas_tiempo,
        'chart_series_tiempo': chart_series_tiempo,
        'chart_peliculas_generos': chart_peliculas_generos,
        'chart_series_generos': chart_series_generos,
    })


# ============================
# Gráficas y Estadísticas Admin
# ============================


@login_required
@user_passes_test(lambda user: user.is_staff)
def graficas_y_stats(request):
    # Datos del Resumen
    total_usuarios = Usuario.objects.count()
    total_peliculas = Pelicula.objects.count()
    total_series = Serie.objects.count()

    # Datos de Usuarios por Rol
    usuarios_por_rol = Usuario.objects.values('role').annotate(total=Count('id'))
    roles = [usuario['role'] for usuario in usuarios_por_rol]
    roles_count = [usuario['total'] for usuario in usuarios_por_rol]

    # Gráfico de Roles
    grafico_usuarios = go.Figure(data=[go.Pie(labels=roles, values=roles_count, hole=0.4)])
    grafico_usuarios.update_layout(
        title="Distribución de Roles",
        height=300,
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )
    grafico_usuarios = grafico_usuarios.to_html(full_html=False)

    # Películas más vistas
    peliculas_mas_vistas = Pelicula.objects.filter(vistas_totales__gt=0).order_by('-vistas_totales')[:5]
    peliculas_titulos = [pelicula.titulo for pelicula in peliculas_mas_vistas]
    peliculas_vistas = [pelicula.vistas_totales for pelicula in peliculas_mas_vistas]

    grafico_peliculas = go.Figure(data=[
        go.Bar(
            y=peliculas_titulos,
            x=peliculas_vistas,
            orientation='h',
            marker=dict(color='rgba(58, 71, 80, 0.6)', line=dict(color='rgba(58, 71, 80, 1.0)', width=2))
        )
    ])
    grafico_peliculas.update_layout(
        title="Películas Más Vistas",
        xaxis_title="Vistas Totales",
        yaxis_title="Películas",
        template="plotly_dark",
        height=400,
        font=dict(color="white")
    )
    grafico_peliculas = grafico_peliculas.to_html(full_html=False)

    # Series más vistas
    series_mas_vistas = Serie.objects.filter(vistas_totales__gt=0).order_by('-vistas_totales')[:5]
    series_titulos = [serie.titulo for serie in series_mas_vistas]
    series_vistas = [serie.vistas_totales for serie in series_mas_vistas]

    grafico_series = go.Figure(data=[
        go.Bar(
            y=series_titulos,
            x=series_vistas,
            orientation='h',
            marker=dict(color='rgba(246, 78, 139, 0.6)', line=dict(color='rgba(246, 78, 139, 1.0)', width=2))
        )
    ])
    grafico_series.update_layout(
        title="Series Más Vistas",
        xaxis_title="Vistas Totales",
        yaxis_title="Series",
        template="plotly_dark",
        height=400,
        font=dict(color="white")
    )
    grafico_series = grafico_series.to_html(full_html=False)

    # Películas y series favoritas
    peliculas_favoritas = Pelicula.objects.annotate(
        total_favoritos=Count('usuarios_pelicula', filter=Q(usuarios_pelicula__favorito=True))
    ).filter(total_favoritos__gt=0).order_by('-total_favoritos')[:5]

    series_favoritas = Serie.objects.annotate(
        total_favoritos=Count('usuarios_serie', filter=Q(usuarios_serie__favorito=True))
    ).filter(total_favoritos__gt=0).order_by('-total_favoritos')[:5]

    peliculas_titulos_fav = [pelicula.titulo for pelicula in peliculas_favoritas]
    peliculas_favoritos = [pelicula.total_favoritos for pelicula in peliculas_favoritas]

    series_titulos_fav = [serie.titulo for serie in series_favoritas]
    series_favoritos = [serie.total_favoritos for serie in series_favoritas]

    grafico_favoritos = go.Figure()

    grafico_favoritos.add_trace(go.Bar(
        y=peliculas_titulos_fav,
        x=peliculas_favoritos,
        name='Películas Favoritas',
        orientation='h',
        marker=dict(color='rgba(0, 204, 150, 0.6)', line=dict(color='rgba(0, 204, 150, 1.0)', width=2))
    ))

    grafico_favoritos.add_trace(go.Bar(
        y=series_titulos_fav,
        x=series_favoritos,
        name='Series Favoritas',
        orientation='h',
        marker=dict(color='rgba(255, 102, 102, 0.6)', line=dict(color='rgba(255, 102, 102, 1.0)', width=2))
    ))

    grafico_favoritos.update_layout(
        title="Películas y Series Favoritas",
        xaxis_title="Número de Favoritos",
        yaxis_title="Contenidos",
        barmode='group',
        template="plotly_dark",
        height=400,
        font=dict(color="white")
    )
    grafico_favoritos = grafico_favoritos.to_html(full_html=False)

    # Tabla de usuarios
    usuarios = Usuario.objects.annotate(
        contador_peliculas_vistas=Count('mi_lista', filter=Q(mi_lista__pelicula__isnull=False, mi_lista__visto=True)),
        contador_series_vistas=Count('mi_lista', filter=Q(mi_lista__serie__isnull=False, mi_lista__visto=True))
    )

    context = {
        'total_usuarios': total_usuarios,
        'total_peliculas': total_peliculas,
        'total_series': total_series,
        'grafico_usuarios': grafico_usuarios,
        'grafico_peliculas': grafico_peliculas,
        'grafico_series': grafico_series,
        'grafico_favoritos': grafico_favoritos,
        'usuarios': usuarios,
    }

    return render(request, 'usuarios/graficas_y_stats.html', context)

@login_required
@user_passes_test(lambda user: user.is_staff)
def estadisticas_usuario_admin(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    # Métricas individuales
    peliculas_vistas = usuario.mi_lista.filter(pelicula__isnull=False, visto=True).count()
    series_vistas = usuario.mi_lista.filter(serie__isnull=False, visto=True).count()

    # Tiempo dedicado (Películas y Series)
    tiempo_peliculas = usuario.mi_lista.filter(pelicula__isnull=False, visto=True).aggregate(total=Sum('pelicula__duracion'))['total'] or 0
    tiempo_series = usuario.mi_lista.filter(serie__isnull=False, visto=True).aggregate(total=Sum('serie__duracion_media_capitulo'))['total'] or 0

    # Distribución de géneros (Películas)
    peliculas_generos = usuario.mi_lista.filter(pelicula__isnull=False, visto=True).values('pelicula__genero').annotate(total=Count('pelicula__genero'))
    series_generos = usuario.mi_lista.filter(serie__isnull=False, visto=True).values('serie__genero').annotate(total=Count('serie__genero'))

    # Estilo general de las gráficas
    layout_estilo = go.Layout(
        paper_bgcolor='rgba(31, 41, 55, 1)',  # Fondo general
        plot_bgcolor='rgba(31, 41, 55, 1)',   # Fondo del área de la gráfica
        font=dict(color="white"),            # Texto blanco
        title_font=dict(size=16, color="white"),  # Títulos más pequeños
        height=300,
        width=400,
    )

    # Gráfica 1: Tiempo en Películas
    fig_peliculas_tiempo = go.Figure(go.Indicator(
        mode="gauge+number",
        value=tiempo_peliculas,
        title={'text': "Minutos en Películas"},
        gauge={
            'axis': {'range': [None, max(tiempo_peliculas * 1.2, 1000)]},
            'bar': {'color': "green"},
        }
    ))
    fig_peliculas_tiempo.update_layout(layout_estilo)

    # Gráfica 2: Tiempo en Series
    fig_series_tiempo = go.Figure(go.Indicator(
        mode="gauge+number",
        value=tiempo_series,
        title={'text': "Minutos en Series"},
        gauge={
            'axis': {'range': [None, max(tiempo_series * 1.2, 1000)]},
            'bar': {'color': "blue"},
        }
    ))
    fig_series_tiempo.update_layout(layout_estilo)

    # Gráfica 3: Distribución de Géneros (Películas)
    fig_peliculas_generos = go.Figure(data=[go.Pie(
        labels=[item['pelicula__genero'] for item in peliculas_generos],
        values=[item['total'] for item in peliculas_generos],
        hole=.4  # Gráfica tipo "donut"
    )])
    fig_peliculas_generos.update_layout(layout_estilo, title="Distribución de Géneros en Películas")

    # Gráfica 4: Distribución de Géneros (Series)
    fig_series_generos = go.Figure(data=[go.Pie(
        labels=[item['serie__genero'] for item in series_generos],
        values=[item['total'] for item in series_generos],
        hole=.4  # Gráfica tipo "donut"
    )])
    fig_series_generos.update_layout(layout_estilo, title="Distribución de Géneros en Series")

    # Convertir gráficos a HTML
    chart_peliculas_tiempo = fig_peliculas_tiempo.to_html(full_html=False)
    chart_series_tiempo = fig_series_tiempo.to_html(full_html=False)
    chart_peliculas_generos = fig_peliculas_generos.to_html(full_html=False)
    chart_series_generos = fig_series_generos.to_html(full_html=False)

    return render(request, 'usuarios/estadisticas_usuario.html', {
        'usuario': usuario,
        'peliculas_vistas': peliculas_vistas,
        'series_vistas': series_vistas,
        'tiempo_peliculas': tiempo_peliculas,
        'tiempo_series': tiempo_series,
        'chart_peliculas_tiempo': chart_peliculas_tiempo,
        'chart_series_tiempo': chart_series_tiempo,
        'chart_peliculas_generos': chart_peliculas_generos,
        'chart_series_generos': chart_series_generos,
    })
