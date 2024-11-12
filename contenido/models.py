from django.db import models

class Contenido(models.Model):
    TIPO_CHOICES = [
        ('pelicula', 'Película'),
        ('serie', 'Serie')
    ]

    GENRE_CHOICES = [
        ('accion', 'Acción'),
        ('comedia', 'Comedia'),
        ('drama', 'Drama'),
        ('terror', 'Terror'),
        ('romance', 'Romance'),
        ('ciencia_ficcion', 'Ciencia Ficción'),
        ('fantasia', 'Fantasía'),
        ('misterio', 'Misterio'),
        ('suspenso', 'Suspenso'),
        ('animacion', 'Animación'),
        ('documental', 'Documental'),
        ('biografia', 'Biografía'),
        ('musical', 'Musical'),
        ('historico', 'Histórico'),
        ('aventura', 'Aventura'),
        ('guerra', 'Guerra'),
        ('crimen', 'Crimen'),
        ('familiar', 'Familiar'),
        ('anime', 'Anime'),
    ]

    # Nuevo campo para marcar contenido destacado
    titulo = models.CharField(max_length=255)
    sinopsis = models.TextField()
    estreno = models.CharField(max_length=4, null=True, blank=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='pelicula')
    genero = models.CharField(max_length=100, choices=GENRE_CHOICES, null=True, blank=True)
    image_cover = models.ImageField(upload_to='content_images/', blank=True, null=True)
    duracion = models.PositiveIntegerField(null=True, blank=True)
    director = models.CharField(max_length=255, blank=True, null=True)
    protagonistas = models.TextField(blank=True, null=True)
    calificacion_usuario = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    vistas_totales = models.IntegerField(default=0)


    def __str__(self):
        return self.titulo
