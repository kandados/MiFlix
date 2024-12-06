from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from ClonFlixApp.models import Pelicula, Serie
from django.utils.timezone import now



class Usuario(AbstractUser):
    """Modelo extendido de usuario para incluir roles y correo electrónico único."""
    ADMIN = 'ADMIN'
    CLIENT = 'CLIENT'
    ROLE_CHOICES = [
        (ADMIN, 'Administrador'),
        (CLIENT, 'Cliente'),
        ('USER', 'USUARIO'),
    ]
    is_first_login = models.BooleanField(default=True)  # Campo que indica si es el primer login
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=CLIENT)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class UsuarioContenido(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mi_lista")
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, null=True, blank=True, related_name="usuarios_pelicula")
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, null=True, blank=True, related_name="usuarios_serie")
    fecha_agregado = models.DateTimeField(default=now)
    favorito = models.BooleanField(default=False)
    visto = models.BooleanField(default=False)
    calificacion = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('usuario', 'pelicula', 'serie')

    def __str__(self):
        if self.pelicula:
            return f"{self.usuario.username} - {self.pelicula.titulo}"
        if self.serie:
            return f"{self.usuario.username} - {self.serie.titulo}"
        return f"{self.usuario.username}"


class Calificacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, null=True, blank=True, on_delete=models.CASCADE)
    serie = models.ForeignKey(Serie, null=True, blank=True, on_delete=models.CASCADE)
    calificacion = models.PositiveSmallIntegerField()  # Valor entre 1 y 10

    class Meta:
        unique_together = ('usuario', 'pelicula', 'serie')  # Evita calificaciones duplicadas
        verbose_name = "Calificación"
        verbose_name_plural = "Calificaciones"

    def __str__(self):
        if self.pelicula:
            return f"{self.usuario.username} calificó {self.pelicula.titulo} con {self.calificacion} estrellas"
        return f"{self.usuario.username} calificó {self.serie.titulo} con {self.calificacion} estrellas"
