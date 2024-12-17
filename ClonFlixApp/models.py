from django.db import models

class Pelicula(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    sinopsis = models.TextField(blank=True, null=True)
    estreno = models.IntegerField(blank=True, null=True)
    genero = models.CharField(max_length=100, blank=True, null=True)
    director = models.CharField(max_length=255, blank=True, null=True)
    protagonistas = models.TextField(blank=True, null=True)
    duracion = models.IntegerField(blank=True, null=True)  # En minutos
    calificacion_usuario = models.FloatField(blank=True, null=True)
    vistas_totales = models.IntegerField(default=0)
    image_cover = models.ImageField(upload_to='movie_images/', blank=True, null=True)

    class Meta:
        db_table = 'Peliculas'
        verbose_name = "Película"
        verbose_name_plural = "Películas"

    def __str__(self):
        return self.titulo


class Serie(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    sinopsis = models.TextField(blank=True, null=True)
    estreno = models.IntegerField(blank=True, null=True)
    genero = models.CharField(max_length=100, blank=True, null=True)
    director = models.CharField(max_length=255, blank=True, null=True)
    protagonistas = models.TextField(blank=True, null=True)
    temporadas_totales = models.IntegerField(blank=True, null=True)
    capitulos_totales = models.IntegerField(blank=True, null=True)
    duracion_media_capitulo = models.IntegerField(blank=True, null=True)  # En minutos
    calificacion_usuario = models.IntegerField(blank=True, null=True)
    vistas_totales = models.IntegerField(default=0)
    image_cover = models.ImageField(upload_to='series_images/', blank=True, null=True)

    class Meta:
        db_table = 'Series'
        verbose_name = "Serie"
        verbose_name_plural = "Series"

    def __str__(self):
        return self.titulo
