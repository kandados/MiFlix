from django.contrib.auth.models import AbstractUser
from django.db import models
from contenido.models import Contenido  # Importar Contenido

class Usuario(AbstractUser):
    ADMIN = 'ADMIN'
    CLIENT = 'CLIENT'
    ROLE_CHOICES = [
        (ADMIN, 'Administrador'),
        (CLIENT, 'Cliente'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=CLIENT)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class UsuarioContenido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE)
    favorito = models.BooleanField(default=False)
    visto = models.BooleanField(default=False)
    ver_mas_tarde = models.BooleanField(default=False)

    class Meta:
        unique_together = ('usuario', 'contenido')

    def __str__(self):
        return f"{self.usuario.username} - {self.contenido.titulo}"
