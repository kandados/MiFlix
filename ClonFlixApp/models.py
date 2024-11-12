from django.db import models
from django.conf import settings

class Movie(models.Model):
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
    # Campos para las peliculas
    title = models.CharField(max_length=255)
    description = models.TextField()  # Sinopsis de la película
    release_date = models.DateField()
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES)
    length = models.PositiveIntegerField()  # Duración en minutos
    image_card = models.ImageField(upload_to='movie_images/')
    image_cover = models.ImageField(upload_to='movie_images/')
    video = models.FileField(upload_to='movie_videos/')
    movie_views = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)  # Campo para películas destacadas
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='pelicula')  # Campo para diferenciar películas y series
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, default=0.0)

    # Campos adicionales para las series
    temporadas_totales = models.PositiveIntegerField(null=True, blank=True)
    capitulos_totales = models.PositiveIntegerField(null=True, blank=True)

    # Nuevos campos para detalles adicionales de películas
    director = models.CharField(max_length=255, default="Desconocido")  # Nombre del director con valor predeterminado
    actors = models.CharField(max_length=500, default="Desconocido")  # Lista de actores principales, separados por comas
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)  # Calificación promedio de usuario (1-5)


class MovieList(models.Model):
    owner_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return self.title