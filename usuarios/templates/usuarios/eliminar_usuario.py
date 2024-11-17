<h1>Confirmar eliminación</h1>
<p>¿Estás seguro de que deseas eliminar al usuario {{ usuario.username }}?</p>

<form method="POST">
    {% csrf_token %}
    <button type="submit">Eliminar</button>
    <a href="{% url 'usuarios:gestion_usuarios' %}">Cancelar</a>
</form>
